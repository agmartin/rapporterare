import uuid

from typing import List, Tuple

from sqlalchemy import or_
from sqlalchemy.sql import text
from utils import SessionLocal
from models import User, UserPostsCleaned


class DataResults:
    def __init__(
        self,
        month: str,
        year: int,
        influencers_with_activity: int,
        posts: int,
        post_mentions: int,
        photo_tags: int,
        actual_reach: int,
        engagement: str,
        likes: int,
        comments: int,
        hashtags: dict[str, int],
        influencer_data: List[Tuple],
    ) -> None:
        self.month = month
        self.year = year
        self.influencers_with_activity = influencers_with_activity
        self.posts = posts
        self.post_mentions = post_mentions
        self.photo_tags = photo_tags
        self.actual_reach = actual_reach
        self.engagement = engagement
        self.likes = likes
        self.comments = comments
        self.hashtags = hashtags
        self.influencer_data = influencer_data


class DataManager:
    def __init__(
        self,
        month_search: str = "January",
        search_terms: List[str] = ["#bubbleroom", "#bubbleroomstyle", "@bubbleroom"],
    ) -> None:
        self.month_search = month_search
        self.search_terms = search_terms
        self.session = SessionLocal()
        self.filtered_results_query = self.generate_filtered_results_query()

    def generate_filtered_results_query(self):
        search_args = [
            UserPostsCleaned.caption_text.like(f"%{term}%")
            for term in self.search_terms
        ]

        filtered_results_query = (
            self.session.query(User, UserPostsCleaned)
            .join(UserPostsCleaned)
            .filter(UserPostsCleaned.month_name == self.month_search)
            .filter(or_(*search_args))
        )

        return filtered_results_query

    def get_filtered_results(self) -> List[Tuple[User, UserPostsCleaned]]:
        filtered_results = self.filtered_results_query.all()
        return filtered_results

    def create_filtered_tmp_table(self) -> bool:
        compiled_filtered_query = str(
            self.filtered_results_query.statement.compile(
                compile_kwargs={"literal_binds": True}
            )
        ).replace("\n", "")

        self.filtered_table_name = f"tmp_report_filtered_{uuid.uuid4()}".replace(
            "-", ""
        )

        create_statement = (
            f"CREATE TABLE {self.filtered_table_name} AS " + compiled_filtered_query
        )

        self.session.execute(text(create_statement))

        return True

    def get_influencer_data(self):
        influencer_query = f"""SELECT
            ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as Rank,
            ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) || '. ' || ig_username as Influencers,
            ig_num_followers AS Followers,
            --likes + comments / followers
            printf("%.2f", (cast((like_count + comment_count) AS REAL) / ig_num_followers) * 100) || '%' as Engagement_General,
            --Engagement (Specific) = likes + comments / followers of brand mentions
            CASE WHEN caption_text LIKE '%@%' THEN printf("%.2f", (cast((like_count + comment_count) AS REAL) / ig_num_followers) * 100) || '%'
                ELSE '0.00%' END AS Engagement_Specific,
            SUM(comment_count) AS Comments,
            SUM(like_count) AS Likes,
            COUNT(*) AS Posts,
            SUM(CASE WHEN caption_text LIKE '%@%' THEN 1 ELSE 0 END) AS Post_Mentions,
            SUM(CASE WHEN caption_text LIKE '%#%' THEN 1 ELSE 0 END) AS Post_Hashtags,
            SUM(CASE WHEN caption_tags IS NOT NULL THEN 1 ELSE 0 END) AS Photo_Tags,

            SUM(CASE WHEN caption_text LIKE '%@%' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN caption_text LIKE '%#%' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN caption_tags IS NOT NULL THEN 1 ELSE 0 END) AS Score
            FROM {self.filtered_table_name}
            GROUP BY ig_username
            ORDER BY Rank;"""

        results_raw = self.session.execute(text(influencer_query)).all()
        headers = [
            "Influencers",
            "Followers",
            "Engagement (General)",
            "Engagement (Specific)",
            "Comments",
            "Likes",
            "Posts",
            "Post Mentions",
            "Post Hashtags",
            "Photo Tags",
            "Score",
        ]

        results_cleaned = [row[1:] for row in results_raw]
        results_cleaned.insert(0, headers)
        return results_cleaned

    def get_aggregates(self):
        aggs_query = f"""SELECT
            COUNT(DISTINCT ig_username) as influencers_with_activity,
            COUNT(*) as posts,
            COUNT(CASE WHEN caption_text LIKE '%@%' THEN 1 ELSE NULL END) as mentions,
            COUNT(CASE WHEN caption_tags IS NOT NULL THEN 1 ELSE NULL END) as photos,
            printf("%.2f", (cast((like_count + comment_count) AS REAL) / ig_num_followers) * 100) || '%' as engagement,
            SUM(like_count) as likes,
            SUM(comment_count) as comments

        FROM {self.filtered_table_name}"""

        results = self.session.execute(text(aggs_query)).all()

        return results[0]

    def get_actual_reach(self):
        actual_reach_query = f"""SELECT SUM(ig_num_followers) as actual_reach
        FROM users
            WHERE id IN (
                SELECT distinct person_id FROM
                {self.filtered_table_name}
                )"""

        results = self.session.execute(text(actual_reach_query)).all()

        return results

    def get_hashtag_data(self, query_data: List[Tuple[User, UserPostsCleaned]]):
        hashtag_dict = {}
        for search_term in self.search_terms:
            if "@" in search_term:
                continue
            hashtag_dict[search_term] = len(
                [
                    row[1].caption_text
                    for row in query_data
                    if search_term in row[1].caption_text
                ]
            )
        return hashtag_dict

    def cleanup(self) -> bool:
        cleanup_query = f"""DROP TABLE IF EXISTS {self.filtered_table_name};"""
        self.session.execute(text(cleanup_query))

    def marshall_data(self) -> DataResults:
        self.create_filtered_tmp_table()
        all_data = self.get_filtered_results()
        influencer_data = self.get_influencer_data()
        aggs = self.get_aggregates()
        reach = self.get_actual_reach()
        hashtags = self.get_hashtag_data(all_data)
        self.cleanup()

        new_dr = DataResults(
            month=self.month_search,
            # add year search so this isn't hard coded
            year=2021,
            influencers_with_activity=aggs[0],
            posts=aggs[1],
            post_mentions=aggs[2],
            photo_tags=aggs[3],
            actual_reach=reach[0][0],
            engagement=aggs[4],
            likes=aggs[5],
            comments=aggs[6],
            hashtags=hashtags,
            influencer_data=influencer_data,
        )

        return new_dr

SELECT * FROM tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b


--Need Rank || UserName, Followers, Engagement (General), Engagement (Specific), Comments, Likes, Posts,
--Post Mentions, Post Hashtags, Photo Tags, Score

SELECT
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
    FROM tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b
    GROUP BY ig_username
    ORDER BY Rank;




SELECT
    COUNT(DISTINCT ig_username) as influencers_with_activity,
    COUNT(*) as posts,
    COUNT(CASE WHEN caption_text LIKE '%@%' THEN 1 ELSE NULL END) as mentions,
    COUNT(CASE WHEN caption_tags IS NOT NULL THEN 1 ELSE NULL END) as photos,
    printf("%.2f", (cast((like_count + comment_count) AS REAL) / ig_num_followers) * 100) as engagement,
    SUM(like_count) as likes,
    SUM(comment_count) as comments

FROM tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b

tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b

SELECT
    printf("%.2f", (cast((like_count + comment_count) AS REAL) / ig_num_followers) * 100) as engagement,
    SUM(like_count) as likes,
    SUM(comment_count) as comments

FROM tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b

--2087359

SELECT SUM(ig_num_followers) as actual_reach
FROM users
    WHERE id IN (
        SELECT distinct person_id FROM
        tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b
        )

--1238392


SELECT * FROM
tmp_report_filtered_8898ddf7f27b41ac9987317134ed4d6b
WHERE caption_text LIKE '%#bubbleroom%'


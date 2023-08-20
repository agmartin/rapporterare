from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode


from data_manager import DataManager

dm = DataManager()

report_data = dm.marshall_data()


class BubbleroomReport(FPDF):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        # Font stuff
        self.add_font("Roboto", "", "./fonts/Roboto-Regular.ttf", uni=True)
        self.add_font("Roboto", "B", "./fonts/Roboto-Bold.ttf", uni=True)
        self.add_font("Roboto", "BI", "./fonts/Roboto-BoldItalic.ttf", uni=True)
        self.add_font("Roboto", "I", "./fonts/Roboto-Italic.ttf", uni=True)
        self.set_font("Roboto", "", 8)

    def header(self):
        pass

    def footer(self):
        self.set_y(-10)
        # self.image("./assets/bubble(700x100).png")

        # Add a page number
        self.set_font("Roboto", "I", 6)
        page = "Page " + str(self.page_no()) + "/{nb}"
        self.cell(0, 10, page, 0, 0, "C")


def create_report():
    pdf = BubbleroomReport()

    pdf.add_page("L")
    pdf.image("./assets/cover.png", 10, 8, 277)
    pdf.set_font("Roboto", "B", 24)
    pdf.set_xy(90, 100)
    pdf.cell(100, 10, "Dev Test Report Bubbleroom", ln=1)
    pdf.set_font("Roboto", "", 16)
    pdf.set_xy(90, 120)
    pdf.cell(100, 10, f"{report_data.month}    {report_data.year}", ln=1)
    pdf.set_x(90)
    pdf.cell(
        100, 10, f"Based on {report_data.influencers_with_activity} influencers", ln=1
    )

    pdf.add_page("L")
    pdf.set_font("Roboto", "B", 24)
    pdf.set_xy(90, 50)
    pdf.cell(100, 10, "Summary Data", ln=1)
    pdf.set_font("Roboto", "", 10)
    pdf.set_xy(90, 60)
    pdf.cell(
        100,
        10,
        f"Influencers with activity    {report_data.influencers_with_activity}",
        ln=1,
    )
    pdf.set_x(90)
    pdf.cell(
        100,
        10,
        f"Posts    {report_data.posts}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Post Mentions    {report_data.post_mentions}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Photo Tags    {report_data.photo_tags}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Actual Reach    {report_data.actual_reach}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Engagement    {report_data.engagement}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Likes    {report_data.likes}",
        ln=1,
    )
    pdf.set_x(90)

    pdf.cell(
        100,
        10,
        f"Comments    {report_data.comments}",
        ln=1,
    )
    pdf.set_x(90)

    # Styled table:
    pdf.add_page("L")
    pdf.set_font("Roboto", "", 8)
    pdf.set_draw_color(255, 0, 0)
    pdf.set_line_width(0.3)
    headings_style = FontFace(emphasis="BOLD", color=0, fill_color=(255, 255, 255))

    with pdf.table(
        borders_layout="NONE",
        cell_fill_color=(211, 211, 211),
        cell_fill_mode=TableCellFillMode.ROWS,
        col_widths=(100, 50, 100, 100, 50, 40, 40, 60, 60, 50, 50, 50),
        headings_style=headings_style,
        line_height=6,
        text_align=(
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
            "LEFT",
        ),
        width=277,
    ) as table:
        for data_row in report_data.influencer_data:
            row = table.row()
            for datum in data_row:
                row.cell(str(datum))

    pdf.output("./report_pdfs/test.pdf")

"""generates a simple PDF report from the analysis results. uses matplotlib for the chart and reportlab for the PDF."""

import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet

def make_bar_chart(analysis: dict):
    #gráfico de barras de los resultados y lo devuelve como PNG
    dist = analysis["distribution"]
    num_dice = analysis["num_dice"]

    #show full expected range even if some values have 0 count
    expected_range = list(range(1, 7)) if num_dice == 1 else list(range(7, 13))
    counts = [dist.get(v, 0) for v in expected_range]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar(expected_range, counts)
    ax.set_xlabel("Result")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Results")
    ax.set_xticks(expected_range)
    fig.tight_layout()

    chart_image = io.BytesIO()
    fig.savefig(chart_image, format="png", dpi=150)
    chart_image.seek(0)
    data = chart_image.read()
    chart_image.close()
    plt.close(fig)
    return data


def build_results_table(analysis: dict) -> list:
    """build the raw rolls table data: one row per throw."""
    num_dice = analysis["num_dice"]
    rolls = analysis["rolls"]
    results = analysis["results"]

    if num_dice == 1:
        header = ["Throw", "Die", "Result"]
        rows = [header]
        for i, (roll, result) in enumerate(zip(rolls, results)):
            rows.append([str(i + 1), str(roll[0]), str(result)])
    else:
        header = ["Throw", "Die 1", "Die 2", "Result"]
        rows = [header]
        for i, (roll, result) in enumerate(zip(rolls, results)):
            rows.append([str(i + 1), str(roll[0]), str(roll[1]), str(result)])

    return rows


def generate_report(analysis: dict, output_path: str):
    """build and save the PDF."""
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_h1 = styles["Heading1"]
    style_h2 = styles["Heading2"]

    story = []

    # title
    story.append(Paragraph("Dice Simulator Report", style_h1))
    dice_label = "1 die" if analysis["num_dice"] == 1 else "2 dice"
    story.append(Paragraph(
        f"Throws: {analysis['num_throws']}  |  Dice: {dice_label}",
        style_normal
    ))
    story.append(Spacer(1, 0.4 * cm))

    # results
    if analysis["num_throws"] <= 100:
        story.append(Paragraph("Results", style_h2))
        table_data = build_results_table(analysis)
        t = Table(table_data, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, -1), 10),
            ("TOPPADDING",   (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
            ("LEFTPADDING",  (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4 * cm))
    else:
        story.append(Paragraph("Results", style_h2))
        story.append(Paragraph(
            f"(Table omitted — {analysis['num_throws']} throws is too large to display row by row.)",
            style_normal
        ))
        story.append(Spacer(1, 0.4 * cm))

    # bar chart
    chart_bytes = make_bar_chart(analysis)
    img = RLImage(io.BytesIO(chart_bytes))
    img.drawWidth  = 14 * cm
    img.drawHeight = 7 * cm
    story.append(img)
    story.append(Spacer(1, 0.5 * cm))

    # q&a
    story.append(Paragraph("Analysis Questions", style_h2))

    def qa(question: str, answer: str):
        story.append(Paragraph(f"<b>{question}</b>", style_normal))
        story.append(Paragraph(answer, style_normal))
        story.append(Spacer(1, 0.3 * cm))

    # Q1 
    dist = analysis["distribution"]
    dist_text = "  ".join(f"Result {v}: {c} times" for v, c in sorted(dist.items()))
    qa("1. What is the distribution of total results?", dist_text)

    # Q2 
    most_v, most_c = analysis["most_frequent"]
    least_v, least_c = analysis["least_frequent"]
    qa("2. What is the most and what is the least frequent result?",
       f"Most frequent: {most_v} ({most_c} times).  Least frequent: {least_v} ({least_c} times).")

    # Q3
    emp = analysis["empirical_probabilities"]
    emp_text = "  ".join(f"Result {v}: {p:.2%}" for v, p in sorted(emp.items()))
    qa("3. What is the empirical probability of rolling each number?", emp_text)

    # Q4 
    qa("4. What's the average, min, and max result?",
       f"Average: {analysis['average']}  |  Min: {analysis['minimum']}  |  Max: {analysis['maximum']}")

    # Q5 
    if analysis["num_dice"] == 1:
        ev = analysis["evenness"]
        qa("5. How evenly distributed are the results of a single dice?",
           f"Max count difference between faces: {ev['max_diff']} — results are {ev['verdict']}.")
    else:
        qa("5. How evenly distributed are the results of a single dice?",
           "Not applicable when throwing two dice (the sum follows a triangular distribution).")

    # Q6 
    if analysis["num_dice"] == 2:
        qa("6. What percentage of rolls were doubles?",
           f"{analysis['doubles_percentage']}% of rolls were doubles.")
    else:
        qa("6. What percentage of rolls were doubles?",
           "Not applicable when throwing one die.")

    # Q7 
    qa("7. What are the percentage of having pairs (even results)?",
       f"{analysis['even_percentage']}% of results were even numbers.")

    # Q8 
    qa("8. What are the percentage of having odds?",
       f"{analysis['odd_percentage']}% of results were odd numbers.")

    #build PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    doc.build(story)
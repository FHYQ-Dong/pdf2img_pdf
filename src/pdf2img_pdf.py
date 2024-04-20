import fitz, os, tqdm, argparse


def pdf2img_pdf(source_path: str, dest_path: str, zoom: int) -> None:
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    source_pdf = fitz.open(source_path)
    tbar = tqdm.tqdm(total=source_pdf.page_count, desc=f"Converting {source_path} to {dest_path}")
    dest_pdf = fitz.open()
    zoom_mat = fitz.Matrix(zoom, zoom)
    for pg_idx in range(source_pdf.page_count):
        page_pix = source_pdf[pg_idx].get_pixmap(alpha=True, matrix=zoom_mat)
        img_bytes = page_pix.tobytes("png")
        img_pdf_bytes = fitz.open("pdf", img_bytes).convert_to_pdf()
        img_pdf = fitz.open("pdf", img_pdf_bytes)
        dest_pdf.insert_pdf(img_pdf)
        tbar.update(1)
    dest_pdf.save(dest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Image PDF")
    parser.add_argument("source_pdf", type=str, help="Source PDF file path")
    parser.add_argument("dest_pdf", type=str, help="Destination PDF file path")
    parser.add_argument("--zoom", "-z", type=int, help="Zoom factor")
    args = parser.parse_args().__dict__

    source_pdf = args["source_pdf"]
    dest_pdf = args["dest_pdf"]
    zoom = args["zoom"] if args["zoom"] else 2
    pdf2img_pdf(source_pdf, dest_pdf, zoom)

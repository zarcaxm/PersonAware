from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from app.models import spacy_model, nltk_model, hft_model
import pypandoc
import time
router = APIRouter()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), library: str = Form(...)):
    file_location = f"./{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    output_file_location = file_location.rsplit('.', 1)[0] + '.txt'

    start_conversion_time = time.time()
    pypandoc.convert_file(file_location, 'plain',
                          outputfile=output_file_location)
    end_conversion_time = time.time()
    conversion_time = end_conversion_time - start_conversion_time

    with open(output_file_location, "r", encoding="utf-8") as f:
        text_content = f.read()

    start_processing_time = time.time()
    if library == 'spaCy':
        entities = spacy_model.process_with_spacy(text_content)
    elif library == 'NLTK':
        entities = spacy_model.process_with_spacy(text_content)
    elif library == 'HFT':
        entities = spacy_model.process_with_spacy(text_content)
    else:
        return {"error": "Invalid library chosen."}
    end_processing_time = time.time()
    processing_time = end_processing_time - start_processing_time

    return {
        "info": f"file '{file.filename}' saved and converted to '{output_file_location}'",
        "entities": entities,
        "file conversion time": conversion_time,
        "file processing_time": processing_time
    }


@router.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <label for="library">Choose a library:</label>
    <select name="library" id="library">
      <option value="spaCy">spaCy</option>
      <option value="NLTK">NLTK</option>
      <option value="HFT">HFT</option>
    </select>
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

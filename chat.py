from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()

MODEL = "gemini-flash-lite-latest"
DOCS_FOLDER = Path("docs")


class DocumentLibrary:
    """Loads every PDF in a folder and keeps its text page by page."""

    def __init__(self, folder: Path):
        self.pages = []  # list of (file name, page number, text)
        for pdf_path in sorted(folder.glob("*.pdf")):
            reader = PdfReader(pdf_path)
            for number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    self.pages.append((pdf_path.name, number, text))

    def as_context(self) -> str:
        return "\n\n".join(
            f"[Source: {name}, page {number}]\n{text}"
            for name, number, text in self.pages
        )


class AeroDoc:
    """Chatbot that answers only from the loaded documents."""

    def __init__(self, library: DocumentLibrary):
        instructions = (
            "You are AeroDoc, an assistant for aeronautics documentation. "
            "Answer ONLY using the documents below. "
            "After each answer, cite your sources as (file, page). "
            "If the answer is not in the documents, say you don't know. "
            "Answer in the same language as the user (French or English).\n\n"
            "DOCUMENTS:\n" + library.as_context()
        )
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model=MODEL, config={"system_instruction": instructions}
        )

    def ask(self, question: str) -> str:
        return self.chat.send_message(question).text


def main():
    library = DocumentLibrary(DOCS_FOLDER)
    if not library.pages:
        print("No PDF found. Put at least one PDF in the 'docs' folder.")
        return

    print(f"AeroDoc:  {len(library.pages)} pages loaded (type 'quit' to exit)")
    bot = AeroDoc(library)

    while True:
        question = input("\nYou: ")
        if question.lower() in ("quit", "exit"):
            break
        try:
            print("AeroDoc:", bot.ask(question))
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
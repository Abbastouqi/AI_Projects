"""Read book input rows from Excel or Google Sheets."""
from pathlib import Path
from typing import Any
import openpyxl
import gspread
from google.oauth2.service_account import Credentials
from book_generator.core.config import get_settings
from book_generator.core.logger import logger

REQUIRED_COLS = {"title"}
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _row_to_dict(headers: list[str], row: list[Any]) -> dict:
    return {h.strip().lower(): (str(v).strip() if v else "") for h, v in zip(headers, row)}


def read_excel(file_path: str) -> list[dict]:
    """Return list of row dicts from the first sheet of an Excel file."""
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(c).strip().lower() if c else "" for c in rows[0]]
    result = []
    for row in rows[1:]:
        if not any(row):
            continue
        d = _row_to_dict(headers, list(row))
        if d.get("title"):
            result.append(d)
    logger.info(f"Excel: read {len(result)} rows from {file_path}")
    return result


def read_google_sheets(sheet_id: str, worksheet_index: int = 0) -> list[dict]:
    """Return list of row dicts from a Google Sheet."""
    creds = Credentials.from_service_account_file(
        get_settings().google_sheets_credentials_json, scopes=SCOPES
    )
    gc = gspread.Client(auth=creds)
    sh = gc.open_by_key(sheet_id)
    ws = sh.get_worksheet(worksheet_index)
    records = ws.get_all_records()
    # Normalize keys
    result = [{k.strip().lower(): str(v).strip() for k, v in r.items()} for r in records if r.get("title")]
    logger.info(f"Google Sheets: read {len(result)} rows from sheet {sheet_id}")
    return result


def read_input(source_type: str, source_ref: str) -> list[dict]:
    if source_type == "excel":
        return read_excel(source_ref)
    elif source_type == "google_sheets":
        return read_google_sheets(source_ref)
    raise ValueError(f"Unknown source_type: {source_type}")

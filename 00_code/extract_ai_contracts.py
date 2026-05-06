from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


DEFAULT_DATA_DIR = Path(r"D:\.01_projects\Tenderalpha_world_contract\unified-government-contract-awards")
DEFAULT_OUTPUT_DIR = Path(r"D:\.01_projects\Tenderalpha_world_contract\00_code\ai_contract_outputs")


KEEP_COLUMNS = [
    # identifiers and source
    "ORIGIN",
    "ORIGIN_ID",
    "TENDER_BIZPORTAL_ID",
    "TRANSACTION_BIZPORTAL_ID",
    # contracting government / buyer
    "CONTRACTING_ENTITY_BIZPORTAL_ID",
    "CONTRACTING_ENTITY_NAME",
    "CONTRACTING_ENTITY_COUNTRY",
    "CONTRACTING_ENTITY_STATE",
    "CONTRACTING_ENTITY_LOCATION",
    "CONTRACTING_ENTITY_ADDRESS",
    "CONTRACTING_ENTITY_POSTCODE",
    "CONTRACTING_ENTITY_WEBSITE",
    # tender content and geography
    "TENDER_TITLE",
    "TENDER_DESCRIPTION",
    "TENDER_INDUSTRY_CODES",
    "TENDER_FUNDING_ORIGIN_COUNTRY",
    "TENDER_COUNTRY",
    "TENDER_STATE",
    "TENDER_LOCATION",
    # dates
    "TENDER_DATE_OF_AWARD",
    "TENDER_DATE_OF_DISPATCH",
    "TENDER_MIN_DELIVERY_DATE",
    "TENDER_CONTRACT_START_DATE",
    "TENDER_CONTRACT_END_DATE",
    # values
    "TENDER_CURRENCY",
    "TENDER_POTENTIAL_VALUE_OF_CONTRACT",
    "TENDER_POTENTIAL_VALUE_OF_CONTRACT_USD",
    "TENDER_CURRENT_EVENT_AMOUNT",
    "TENDER_CURRENT_EVENT_AMOUNT_USD",
    "TENDER_VALUE_OF_CONTRACT_TO_DATE",
    "TENDER_VALUE_OF_CONTRACT_TO_DATE_USD",
    "TENDER_BUDGET_EXECUTION_PERCENTAGE_TO_DATE",
    "TENDER_BIDDERS_COUNT",
    # procedure / contract type
    "TENDER_FRAMEWORK",
    "TENDER_TYPE_OF_AUTHORITY",
    "TENDER_TYPE_OF_CONTRACT",
    "TENDER_TYPE_OF_PROCEDURE",
    "TENDER_TYPE_OF_REGULATION",
    "TENDER_TYPE_OF_BID",
    "TENDER_AWARD_CRITERIA",
    "TENDER_TYPE_OF_CONTRACT_PRICING",
    # direct awardee
    "DIRECT_AWARDEE_BIZPORTAL_ID",
    "DIRECT_AWARDEE_NAME",
    "DIRECT_AWARDEE_UIC",
    "DIRECT_AWARDEE_VAT_NUMBER",
    "DIRECT_AWARDEE_COUNTRY",
    "DIRECT_AWARDEE_STATE",
    "DIRECT_AWARDEE_LOCATION",
    "DIRECT_AWARDEE_ADDRESS",
    "DIRECT_AWARDEE_POSTCODE",
    "DIRECT_AWARDEE_WEBSITE",
    "DIRECT_AWARDEE_LISTING_STATUS",
    "DIRECT_AWARDEE_TICKER_SYMBOL",
    "DIRECT_AWARDEE_STOCK_EXCHANGE_MIC",
    "DIRECT_AWARDEE_STOCK_EXCHANGE_NAME",
    "DIRECT_AWARDEE_STOCK_EXCHANGE_COUNTRY",
    "DIRECT_AWARDEE_ISIN_NUMBER",
    "DIRECT_AWARDEE_AMOUNT",
    "DIRECT_AWARDEE_CURRENCY",
    "DIRECT_AWARDEE_USD_AMOUNT",
    # awardee parent
    "AWARDEE_PARENT_BIZPORTAL_ID",
    "AWARDEE_PARENT_NAME",
    "AWARDEE_PARENT_UIC",
    "AWARDEE_PARENT_VAT_NUMBER",
    "AWARDEE_PARENT_COUNTRY",
    "AWARDEE_PARENT_STATE",
    "AWARDEE_PARENT_LOCATION",
    "AWARDEE_PARENT_ADDRESS",
    "AWARDEE_PARENT_POSTCODE",
    "AWARDEE_PARENT_WEBSITE",
    "AWARDEE_PARENT_LISTING_STATUS",
    "AWARDEE_PARENT_TICKER_SYMBOL",
    "AWARDEE_PARENT_STOCK_EXCHANGE_MIC",
    "AWARDEE_PARENT_STOCK_EXCHANGE_NAME",
    "AWARDEE_PARENT_STOCK_EXCHANGE_COUNTRY",
    "AWARDEE_PARENT_ISIN_NUMBER",
]


TEXT_COLUMNS = ["TENDER_TITLE", "TENDER_DESCRIPTION", "TENDER_INDUSTRY_CODES"]

NUMERIC_COLUMNS = [
    "ORIGIN_ID",
    "TENDER_BIZPORTAL_ID",
    "TRANSACTION_BIZPORTAL_ID",
    "CONTRACTING_ENTITY_BIZPORTAL_ID",
    "TENDER_POTENTIAL_VALUE_OF_CONTRACT",
    "TENDER_POTENTIAL_VALUE_OF_CONTRACT_USD",
    "TENDER_CURRENT_EVENT_AMOUNT",
    "TENDER_CURRENT_EVENT_AMOUNT_USD",
    "TENDER_VALUE_OF_CONTRACT_TO_DATE",
    "TENDER_VALUE_OF_CONTRACT_TO_DATE_USD",
    "TENDER_BUDGET_EXECUTION_PERCENTAGE_TO_DATE",
    "TENDER_BIDDERS_COUNT",
    "DIRECT_AWARDEE_BIZPORTAL_ID",
    "DIRECT_AWARDEE_AMOUNT",
    "DIRECT_AWARDEE_USD_AMOUNT",
    "AWARDEE_PARENT_BIZPORTAL_ID",
]

DATE_COLUMNS = [
    "TENDER_DATE_OF_AWARD",
    "TENDER_DATE_OF_DISPATCH",
    "TENDER_MIN_DELIVERY_DATE",
    "TENDER_CONTRACT_START_DATE",
    "TENDER_CONTRACT_END_DATE",
]

TEXT_OUTPUT_COLUMNS = [
    "SOURCE_FILE",
    "SEARCH_TEXT",
    "AI_MATCH_TERMS",
    "AI_REVIEW_LABEL",
    "PROCUREMENT_CONTENT",
]

OUTPUT_COLUMNS = KEEP_COLUMNS + TEXT_OUTPUT_COLUMNS


AI_PATTERNS = {
    "core_ai_en": [
        r"\bAI\b",
        r"\bA\.I\.\b",
        r"artificial intelligence",
        r"machine learning",
        r"deep learning",
        r"generative ai",
        r"\bgenai\b",
        r"large language model",
        r"\bLLM\b",
        r"natural language processing",
        r"\bNLP\b",
        r"computer vision",
        r"neural network",
        r"neural networks",
        r"predictive analytics",
        r"cognitive computing",
        r"intelligent automation",
        r"chatbot",
        r"chat bot",
        r"virtual assistant",
        r"robotic process automation",
        r"\bRPA\b",
        r"data science",
        r"algorithmic decision",
        r"automated decision",
        r"image recognition",
        r"speech recognition",
        r"text analytics",
        r"sentiment analysis",
        r"recommendation engine",
        r"reinforcement learning",
    ],
    "ai_cjk_korean": [
        r"人工智能",
        r"机器学习",
        r"機器學習",
        r"深度学习",
        r"深度學習",
        r"大语言模型",
        r"大語言模型",
        r"自然语言处理",
        r"自然語言處理",
        r"计算机视觉",
        r"計算機視覺",
        r"神经网络",
        r"神經網絡",
        r"智能算法",
        r"生成式AI",
        r"生成式人工智能",
        r"챗봇",
        r"인공지능",
        r"머신러닝",
        r"기계학습",
        r"딥러닝",
        r"자연어 처리",
        r"컴퓨터 비전",
    ],
    "ai_cyrillic": [
        r"искусственн\w* интеллект",
        r"машинн\w* обуч",
        r"глубок\w* обуч",
        r"нейронн\w* сет",
        r"компьютерн\w* зрени",
        r"обработк\w* естественн\w* язык",
        r"чат[ -]?бот",
        r"штучн\w* інтелект",
        r"машинн\w* навчан",
        r"глибок\w* навчан",
        r"нейронн\w* мереж",
    ],
    "ai_western_europe": [
        r"inteligencia artificial",
        r"aprendizaje automatico",
        r"aprendizaje automático",
        r"aprendizaje profundo",
        r"procesamiento del lenguaje natural",
        r"vision artificial",
        r"visión artificial",
        r"red neuronal",
        r"inteligência artificial",
        r"aprendizado de maquina",
        r"aprendizado de máquina",
        r"aprendizagem automatica",
        r"aprendizagem automática",
        r"intelligence artificielle",
        r"apprentissage automatique",
        r"apprentissage profond",
        r"traitement du langage naturel",
        r"vision par ordinateur",
        r"künstliche intelligenz",
        r"kuenstliche intelligenz",
        r"maschinelles lernen",
        r"neuronale netz",
        r"sprachverarbeitung",
    ],
    "ai_eastern_europe": [
        r"sztuczna inteligencja",
        r"uczenie maszynowe",
        r"sieci neuronowe",
        r"inteligenta artificiala",
        r"inteligență artificială",
        r"invatare automata",
        r"învățare automată",
        r"retele neuronale",
        r"rețele neuronale",
        r"umělá inteligence",
        r"strojové učení",
        r"neuronové sítě",
    ],
}


STRONG_AI_RE = re.compile(
    r"artificial intelligence|machine learning|deep learning|generative ai|\bgenai\b|large language model|"
    r"natural language processing|computer vision|neural network|predictive analytics|cognitive computing|"
    r"intelligent automation|chatbot|chat bot|virtual assistant|robotic process automation|data science|"
    r"algorithmic decision|automated decision|image recognition|speech recognition|text analytics|sentiment analysis|"
    r"recommendation engine|reinforcement learning|人工智能|机器学习|機器學習|深度学习|深度學習|大语言模型|大語言模型|"
    r"自然语言处理|自然語言處理|计算机视觉|計算機視覺|神经网络|神經網絡|智能算法|生成式AI|生成式人工智能|"
    r"챗봇|인공지능|머신러닝|기계학습|딥러닝|자연어 처리|컴퓨터 비전|"
    r"искусственн\w* интеллект|машинн\w* обуч|глубок\w* обуч|нейронн\w* сет|компьютерн\w* зрени|"
    r"обработк\w* естественн\w* язык|чат[ -]?бот|штучн\w* інтелект|машинн\w* навчан|глибок\w* навчан|"
    r"нейронн\w* мереж|inteligencia artificial|aprendizaje automatico|aprendizaje automático|aprendizaje profundo|"
    r"procesamiento del lenguaje natural|vision artificial|visión artificial|red neuronal|inteligência artificial|"
    r"aprendizado de maquina|aprendizado de máquina|aprendizagem automatica|aprendizagem automática|intelligence artificielle|"
    r"apprentissage automatique|apprentissage profond|traitement du langage naturel|vision par ordinateur|"
    r"künstliche intelligenz|kuenstliche intelligenz|maschinelles lernen|neuronale netz|sprachverarbeitung|"
    r"sztuczna inteligencja|uczenie maszynowe|sieci neuronowe|inteligenta artificiala|inteligență artificială|"
    r"invatare automata|învățare automată|retele neuronale|rețele neuronale|umělá inteligence|strojové učení|neuronové sítě",
    flags=re.IGNORECASE,
)

ABBREVIATION_RE = re.compile(r"\b(?:AI|A\.I\.|LLM|NLP|RPA)\b")
NON_ENGLISH_AI_WORD_RE = re.compile(
    r"\bai\s+(sensi|fini|sens|faptul|caror|căror|fiecare|fost|centri|siti)\b",
    flags=re.IGNORECASE,
)
AIRCRAFT_PART_AI_RE = re.compile(
    r"\b(aircraft|spacecraft|auxiliary equipment|spare parts|panel,ai|"
    r"plate,?\s*structural,?\s*ai|blade,?\s*compressor,?\s*ai|windshield panel,?\s*ai|"
    r"support assembly,?\s*ai|nut,?\s*self-locking,?\s*ai|adapter,?\s*tie down,?\s*ai)\b",
    flags=re.IGNORECASE,
)
RPA_AIRCRAFT_RE = re.compile(
    r"\b(remotely piloted aircraft|aircraft|squadron|gcs|ground control station|ang|air national guard)\b",
    flags=re.IGNORECASE,
)


AI_PATTERNS["broad_ai_en"] = [
    r"autonomous system",
    r"autonomous systems",
    r"autonomous vehicle",
    r"autonomous vehicles",
    r"autonomous robot",
    r"autonomous robotics",
    r"autonomous navigation",
    r"autonomous fault",
    r"autonomous decision",
    r"autonomy software",
    r"decision support algorithm",
    r"decision support system",
    r"advanced analytics",
    r"big data analytics",
    r"big data analysis",
    r"text mining",
    r"data mining",
    r"pattern recognition",
    r"object detection",
    r"target recognition",
    r"anomaly detection",
    r"fraud detection",
    r"risk prediction",
    r"predictive model",
    r"predictive modeling",
    r"predictive modelling",
    r"forecasting model",
    r"classification model",
    r"recommendation system",
    r"knowledge graph",
    r"expert system",
    r"intelligent system",
    r"intelligent systems",
    r"intelligent video",
    r"smart analytics",
    r"smart surveillance",
    r"facial recognition",
    r"face recognition",
    r"biometric recognition",
    r"optical character recognition",
    r"\bOCR\b",
    r"automatic speech recognition",
    r"voice recognition",
    r"semantic search",
    r"semantic analysis",
    r"automated text analysis",
    r"automated image analysis",
    r"algorithm development",
    r"algorithmic analysis",
    r"model training",
    r"training data",
    r"synthetic data",
    r"data labeling",
    r"data labelling",
    r"annotation services",
    r"model validation",
    r"model evaluation",
    r"MLOps",
    r"computer assisted detection",
    r"computer aided detection",
    r"computer-aided detection",
]

BROAD_AI_RE = re.compile("|".join(AI_PATTERNS["broad_ai_en"]), flags=re.IGNORECASE)


COMPILED_AI_PATTERNS = [
    (group, term, re.compile(term, flags=re.IGNORECASE))
    for group, terms in AI_PATTERNS.items()
    for term in terms
]


def list_parquet_files(data_dir: Path) -> list[Path]:
    return sorted(path for path in data_dir.glob("*.parquet") if not path.name.startswith("._"))


def available_columns(path: Path, requested: list[str]) -> list[str]:
    schema = pq.read_schema(path)
    names = set(schema.names)
    return [col for col in requested if col in names]


def join_search_text(df: pd.DataFrame) -> pd.Series:
    text = pd.Series("", index=df.index, dtype="object")
    for col in TEXT_COLUMNS:
        if col in df.columns:
            text = text.str.cat(df[col].fillna("").astype(str), sep="\n")
    return text


def find_ai_terms(text: str) -> list[str]:
    if not isinstance(text, str) or not text:
        return []
    matches = []
    for group, term, pattern in COMPILED_AI_PATTERNS:
        if pattern.search(text):
            matches.append(f"{group}: {term}")
    return matches


def review_ai_match(text: str) -> str:
    if not isinstance(text, str) or not text:
        return "not_ai_empty_text"

    lower = text.lower()
    has_strong_ai = bool(STRONG_AI_RE.search(text) or BROAD_AI_RE.search(text))
    has_abbreviation = bool(ABBREVIATION_RE.search(text))
    has_rpa = bool(re.search(r"\bRPA\b|robotic process automation", text, flags=re.IGNORECASE))

    if NON_ENGLISH_AI_WORD_RE.search(text) and not has_strong_ai and not has_abbreviation:
        return "false_positive_non_english_ai_word"
    if AIRCRAFT_PART_AI_RE.search(text) and has_abbreviation and not has_strong_ai:
        return "false_positive_aircraft_or_part_code_ai"
    if has_rpa and RPA_AIRCRAFT_RE.search(text) and "robotic process automation" not in lower:
        return "likely_false_positive_rpa_aircraft"
    if has_strong_ai:
        return "clear_ai_related"
    if has_abbreviation:
        return "possible_ai_abbreviation_only"
    return "possible_ai_manual_review"


def classify_procurement_content(text: str) -> str:
    if not isinstance(text, str):
        return "other_manual_review"
    lower = text.lower()

    if AIRCRAFT_PART_AI_RE.search(text):
        return "aircraft_or_mechanical_parts"
    if re.search(r"construction materials|construction|building|engineering studies|energy and related services", lower):
        return "construction_engineering_energy"
    if re.search(r"medical|surgical|laboratory|reagents|health|voice recognition|speech recognition", lower):
        return "medical_lab_or_speech_recognition"
    if re.search(r"food|meat|vegetables|fruit|potatoes|poultry|beef|pork", lower):
        return "food_or_agricultural_supply"
    if re.search(r"cleaning|maintenance|parks maintenance|lift-maintenance|security services|postal|courier", lower):
        return "facility_maintenance_security_postal"
    if re.search(r"research|development|r&d|baa|prototype|study|studies|experimental development", lower):
        return "ai_research_development_or_prototype"
    if re.search(r"software|platform|system|systems design|saas|license|licenses|cloud|computer programming|it services|information systems", lower):
        return "ai_software_platform_or_information_system"
    if re.search(r"data analysis|text mining|analytics|data science|predictive|model|models|algorithm", lower):
        return "ai_data_analysis_modeling_or_algorithm"
    if re.search(r"robotic process automation|intelligent automation|chatbot|virtual assistant|image recognition|speech recognition|voice recognition", lower):
        return "ai_automation_recognition_or_virtual_assistant"
    if re.search(r"consultant|consulting|advisory|strategic partner|training|course|professional services", lower):
        return "ai_consulting_training_or_professional_services"
    if re.search(r"gpu|network interface card|server|hardware|chip|uav|drone|5g", lower):
        return "ai_hardware_compute_or_unmanned_system"
    return "other_manual_review"


def should_keep_review_label(label: str, keep_possible: bool) -> bool:
    if label == "clear_ai_related":
        return True
    if keep_possible and label in {"possible_ai_abbreviation_only", "possible_ai_manual_review"}:
        return True
    return False


def log_progress(message: str, quiet: bool = False) -> None:
    if not quiet:
        print(message, flush=True)


def process_file(path: Path, keep_possible: bool, quiet: bool = False) -> tuple[pd.DataFrame, dict[str, int]]:
    started = time.perf_counter()
    log_progress(f"    reading schema/columns...", quiet)
    columns = available_columns(path, KEEP_COLUMNS)
    t_schema = time.perf_counter()

    log_progress(f"    reading parquet columns={len(columns)}...", quiet)
    df = pd.read_parquet(path, columns=columns)
    t_read = time.perf_counter()

    log_progress(f"    preparing search text for {len(df):,} rows...", quiet)
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    search_text = join_search_text(df)
    t_text = time.perf_counter()

    log_progress("    matching AI keyword candidates...", quiet)
    initial_mask = (
        search_text.str.contains(STRONG_AI_RE, regex=True, na=False)
        | search_text.str.contains(BROAD_AI_RE, regex=True, na=False)
        | search_text.str.contains(ABBREVIATION_RE, regex=True, na=False)
    )
    candidates = df.loc[initial_mask].copy()
    candidate_text = search_text.loc[initial_mask]
    t_match = time.perf_counter()

    if candidates.empty:
        return candidates, {
            "rows_total": len(df),
            "rows_initial_ai_candidates": 0,
            "rows_kept": 0,
            "rows_excluded_false_positive": 0,
            "seconds_schema": round(t_schema - started, 3),
            "seconds_read": round(t_read - t_schema, 3),
            "seconds_text": round(t_text - t_read, 3),
            "seconds_match": round(t_match - t_text, 3),
            "seconds_review": 0.0,
            "seconds_total": round(time.perf_counter() - started, 3),
        }

    log_progress(f"    reviewing {len(candidates):,} candidates and classifying content...", quiet)
    candidates["SOURCE_FILE"] = path.name
    candidates["SEARCH_TEXT"] = candidate_text
    candidates["AI_MATCH_TERMS"] = candidate_text.map(lambda value: "; ".join(find_ai_terms(value)))
    candidates["AI_REVIEW_LABEL"] = candidate_text.map(review_ai_match)
    candidates["PROCUREMENT_CONTENT"] = candidate_text.map(classify_procurement_content)
    t_review = time.perf_counter()

    keep_mask = candidates["AI_REVIEW_LABEL"].map(lambda label: should_keep_review_label(label, keep_possible))
    kept = candidates.loc[keep_mask].copy()

    stats = {
        "rows_total": len(df),
        "rows_initial_ai_candidates": len(candidates),
        "rows_kept": len(kept),
        "rows_excluded_false_positive": len(candidates) - len(kept),
        "seconds_schema": round(t_schema - started, 3),
        "seconds_read": round(t_read - t_schema, 3),
        "seconds_text": round(t_text - t_read, 3),
        "seconds_match": round(t_match - t_text, 3),
        "seconds_review": round(t_review - t_match, 3),
        "seconds_total": round(time.perf_counter() - started, 3),
    }
    return kept, stats


def write_parquet_incremental(writer: pq.ParquetWriter | None, frame: pd.DataFrame, output_path: Path) -> pq.ParquetWriter:
    frame = frame.copy()

    for col in OUTPUT_COLUMNS:
        if col not in frame.columns:
            if col in NUMERIC_COLUMNS:
                frame[col] = pd.NA
            elif col in DATE_COLUMNS:
                frame[col] = pd.NaT
            else:
                frame[col] = ""

    for col in NUMERIC_COLUMNS:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").astype("float64")

    for col in DATE_COLUMNS:
        if col in frame.columns:
            frame[col] = pd.to_datetime(frame[col], errors="coerce")

    # Any remaining non-numeric/non-date columns are treated as text output. This
    # prevents the first written batch from creating an all-null parquet column.
    typed_columns = set(NUMERIC_COLUMNS) | set(DATE_COLUMNS)
    for col in frame.columns:
        if col not in typed_columns:
            frame[col] = frame[col].fillna("").astype(str)

    frame = frame[OUTPUT_COLUMNS]

    table = pa.Table.from_pandas(frame, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(output_path, table.schema, compression="snappy")
    elif table.schema != writer.schema:
        table = table.cast(writer.schema)
    writer.write_table(table)
    return writer


def load_manifest(manifest_path: Path) -> dict[str, dict]:
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup_path = manifest_path.with_suffix(manifest_path.suffix + ".corrupt")
        manifest_path.replace(backup_path)
        print(f"Manifest JSON was corrupt; moved it to {backup_path}", flush=True)
        return {}
    return data.get("files", {})


def save_manifest(manifest_path: Path, completed_files: dict[str, dict]) -> None:
    payload = {
        "updated_at": pd.Timestamp.now().isoformat(),
        "files": completed_files,
    }
    temp_path = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(manifest_path)


def append_summary_row(summary_csv: Path, stats: dict) -> None:
    row = pd.DataFrame([stats])
    row.to_csv(
        summary_csv,
        mode="a",
        index=False,
        header=not summary_csv.exists(),
        encoding="utf-8-sig",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract AI-related UGCA contracts from all parquet files.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-files", type=int, default=None, help="Optional smoke-test limit.")
    parser.add_argument(
        "--keep-possible",
        action="store_true",
        help="Also keep abbreviation-only/manual-review AI candidates. By default only clear AI matches are kept.",
    )
    parser.add_argument("--csv", action="store_true", help="Also write a CSV copy. This can be large.")
    parser.add_argument("--quiet", action="store_true", help="Only print one summary line per file.")
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Clear previous outputs and manifest, then start from the first file.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_parquet = args.output_dir / "ai_contracts_all_files.parquet"
    summary_csv = args.output_dir / "ai_contract_extraction_summary.csv"
    output_csv = args.output_dir / "ai_contracts_all_files.csv"
    manifest_path = args.output_dir / "ai_contract_extraction_manifest.json"

    if args.restart:
        for old_path in [output_parquet, summary_csv, output_csv, manifest_path]:
            if old_path.exists():
                old_path.unlink()

    completed_files = load_manifest(manifest_path)
    if completed_files:
        print(f"Resume mode: {len(completed_files):,} files already completed in manifest.", flush=True)

    files = list_parquet_files(args.data_dir)
    if args.max_files is not None:
        files = files[: args.max_files]
    if not files:
        raise FileNotFoundError(f"No parquet files found in {args.data_dir}")

    pending_files = [path for path in files if path.name not in completed_files]
    if not pending_files:
        print("No pending files. All files in the selected range are already completed.", flush=True)
        if summary_csv.exists():
            summary = pd.read_csv(summary_csv)
            print(f"Summary CSV: {summary_csv}")
            print(f"Rows scanned: {int(summary['rows_total'].sum()):,}")
            print(f"AI contracts kept: {int(summary['rows_kept'].sum()):,}")
        return

    writer: pq.ParquetWriter | None = None
    csv_header_written = output_csv.exists()
    run_started = time.perf_counter()

    try:
        for pending_index, path in enumerate(pending_files, start=1):
            overall_index = files.index(path) + 1
            file_started = time.perf_counter()
            elapsed = file_started - run_started
            avg_per_finished = elapsed / (pending_index - 1) if pending_index > 1 else None
            eta = avg_per_finished * (len(pending_files) - pending_index + 1) if avg_per_finished else None

            print(
                f"\n[{overall_index}/{len(files)} | pending {pending_index}/{len(pending_files)}] starting {path.name} "
                f"(elapsed={elapsed / 60:.1f} min"
                + (f", eta~{eta / 60:.1f} min" if eta is not None else "")
                + ")",
                flush=True,
            )

            kept, stats = process_file(path, keep_possible=args.keep_possible, quiet=args.quiet)
            stats["file"] = path.name

            if not kept.empty:
                log_progress(f"    writing {len(kept):,} kept rows...", args.quiet)
                t_write_start = time.perf_counter()
                writer = write_parquet_incremental(writer, kept, output_parquet)
                if args.csv:
                    kept.to_csv(
                        output_csv,
                        mode="a",
                        index=False,
                        header=not csv_header_written,
                        encoding="utf-8-sig",
                    )
                    csv_header_written = True
                stats["seconds_write"] = round(time.perf_counter() - t_write_start, 3)
            else:
                stats["seconds_write"] = 0.0

            stats["status"] = "completed"
            stats["completed_at"] = pd.Timestamp.now().isoformat()
            completed_files[path.name] = stats
            append_summary_row(summary_csv, stats)
            save_manifest(manifest_path, completed_files)

            finished = time.perf_counter()
            elapsed = finished - run_started
            avg_per_file = elapsed / pending_index
            remaining = avg_per_file * (len(pending_files) - pending_index)

            print(
                f"[{overall_index}/{len(files)}] done {path.name}: "
                f"candidates={stats['rows_initial_ai_candidates']:,}, "
                f"kept={stats['rows_kept']:,}, "
                f"excluded={stats['rows_excluded_false_positive']:,}, "
                f"file_time={finished - file_started:.1f}s, "
                f"avg={avg_per_file:.1f}s/file, "
                f"eta~{remaining / 60:.1f} min"
            )
    finally:
        if writer is not None:
            writer.close()

    summary = pd.read_csv(summary_csv) if summary_csv.exists() else pd.DataFrame()

    total_rows = int(summary["rows_total"].sum()) if not summary.empty else 0
    total_candidates = int(summary["rows_initial_ai_candidates"].sum()) if not summary.empty else 0
    total_kept = int(summary["rows_kept"].sum()) if not summary.empty else 0
    total_excluded = int(summary["rows_excluded_false_positive"].sum()) if not summary.empty else 0

    print("\nDone.")
    print(f"Files selected: {len(files):,}")
    print(f"Files completed in manifest: {len(completed_files):,}")
    print(f"Rows scanned: {total_rows:,}")
    print(f"Initial AI candidates: {total_candidates:,}")
    print(f"AI contracts kept: {total_kept:,}")
    print(f"False positives excluded: {total_excluded:,}")
    print(f"Output parquet: {output_parquet}")
    print(f"Summary CSV: {summary_csv}")
    print(f"Manifest: {manifest_path}")
    if args.csv:
        print(f"Output CSV: {output_csv}")


if __name__ == "__main__":
    main()

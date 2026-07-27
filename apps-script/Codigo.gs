const ROOT_FOLDER_NAME = 'PDF_WHATSAPP';
const PLANOS_SHEET_NAME = 'Planos';

const PLANOS_HEADERS = [
  'Carpeta',
  'ProyectoCodigo',
  'ClienteCodigo',
  'TipoPlanoCodigo',
  'TipoPlano',
  'NombreArchivo',
  'DriveFileId',
  'DriveUrl',
  'FechaModificacion',
  'FechaSincronizacion',
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Planos')
    .addItem('Configurar hoja', 'setup')
    .addItem('Sincronizar desde Drive', 'syncDrivePlans')
    .addToUi();
}

function setup() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = getOrCreateSheet_(spreadsheet, PLANOS_SHEET_NAME);

  sheet.clear();

  sheet
    .getRange(1, 1, 1, PLANOS_HEADERS.length)
    .setValues([PLANOS_HEADERS])
    .setFontWeight('bold');

  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, PLANOS_HEADERS.length);

  SpreadsheetApp.getUi().alert(
    `La hoja "${PLANOS_SHEET_NAME}" fue configurada correctamente.`
  );
}

function syncDrivePlans() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = getOrCreateSheet_(spreadsheet, PLANOS_SHEET_NAME);

  preparePlanosSheet_(sheet);

  const rootFolder = findRootFolder_();
  const projectFolders = rootFolder.getFolders();
  const rows = [];

  while (projectFolders.hasNext()) {
    const projectFolder = projectFolders.next();

    collectProjectFiles_(
      projectFolder,
      projectFolder.getName(),
      rows
    );
  }

  if (rows.length > 0) {
    sheet
      .getRange(2, 1, rows.length, PLANOS_HEADERS.length)
      .setValues(rows);
  }

  sheet.autoResizeColumns(1, PLANOS_HEADERS.length);

  SpreadsheetApp.getUi().alert(
    `Sincronización completa. Planos encontrados: ${rows.length}`
  );
}

function collectProjectFiles_(folder, projectFolderName, rows) {
  const files = folder.getFiles();

  while (files.hasNext()) {
    const file = files.next();

    if (!isPdf_(file)) {
      continue;
    }

    const parsed = parsePlanFileName_(file.getName());

    rows.push([
      projectFolderName,
      parsed.projectCode,
      parsed.clientCode,
      parsed.planTypeCode,
      parsed.planType,
      file.getName(),
      file.getId(),
      file.getUrl(),
      file.getLastUpdated(),
      new Date(),
    ]);
  }

  /*
   * Esta parte permite encontrar planos dentro de subcarpetas
   * adicionales del proyecto.
   */
  const subfolders = folder.getFolders();

  while (subfolders.hasNext()) {
    collectProjectFiles_(
      subfolders.next(),
      projectFolderName,
      rows
    );
  }
}

function parsePlanFileName_(fileName) {
  const cleanName = String(fileName || '')
    .replace(/\.pdf$/i, '')
    .trim();

  const parts = cleanName
    .split('_')
    .map((part) => part.trim())
    .filter(Boolean);

  /*
   * Convención real:
   *
   * MONTAÑO_A01.pdf
   * MONTAÑO_AAC01.pdf
   * MONTAÑO_E01.pdf
   * MONTAÑO_IE01.pdf
   * MONTAÑO_IHS01.pdf
   * MONTAÑO_PYV01.pdf
   */

  const projectCode = parts[0] || '';
  const rawPlanCode = parts[1] || '';

  /*
   * Separa letras y número:
   *
   * A01   -> A + 01
   * AAC01 -> AAC + 01
   * IE01  -> IE + 01
   * IHS01 -> IHS + 01
   */
  const match = rawPlanCode.match(/^([A-ZÁÉÍÓÚÜÑ]+)(\d+)$/i);

  let planTypeCode = rawPlanCode.toUpperCase();

  if (match) {
    planTypeCode = match[1].toUpperCase();
  }

  /*
   * Caso especial:
   * En tus archivos aparece AAC01, pero el catálogo usa AA.
   */
  if (planTypeCode === 'AAC') {
    planTypeCode = 'AA';
  }

  return {
    projectCode: normalizeCode_(projectCode),
    clientCode: normalizeCode_(projectCode),
    planTypeCode: planTypeCode,
    planType: getPlanTypeName_(planTypeCode),
  };
}

function normalizeCode_(value) {
  return String(value || '')
    .trim()
    .toUpperCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

function getPlanTypeName_(code) {
  const normalized = String(code || '')
    .trim()
    .toUpperCase();

  const types = {
    A: "Arquitectónico",
    AA: "Aire acondicionado",
    IS: "Instalación sanitaria",
    IH: "Instalación hidráulica",
    IHS: "Instalación hidrosanitaria",
    IE: "Instalación eléctrica",
    PYV: "Puertas y ventanas",
    E: "Estructural",
  };

  return types[normalized] || 'Desconocido';
}

function findRootFolder_() {
  const folders = DriveApp.getFoldersByName(ROOT_FOLDER_NAME);

  if (!folders.hasNext()) {
    throw new Error(
      `No se encontró la carpeta raíz "${ROOT_FOLDER_NAME}".`
    );
  }

  const rootFolder = folders.next();

  if (folders.hasNext()) {
    throw new Error(
      `Existe más de una carpeta llamada "${ROOT_FOLDER_NAME}". ` +
      'Usaremos posteriormente el ID de la carpeta para evitar ambigüedades.'
    );
  }

  return rootFolder;
}

function preparePlanosSheet_(sheet) {
  sheet.clearContents();

  sheet
    .getRange(1, 1, 1, PLANOS_HEADERS.length)
    .setValues([PLANOS_HEADERS])
    .setFontWeight('bold');

  sheet.setFrozenRows(1);
}

function isPdf_(file) {
  return (
    file.getMimeType() === MimeType.PDF ||
    file.getName().toLowerCase().endsWith('.pdf')
  );
}

function getOrCreateSheet_(spreadsheet, name) {
  return (
    spreadsheet.getSheetByName(name) ||
    spreadsheet.insertSheet(name)
  );
}
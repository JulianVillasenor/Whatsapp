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
   * Convención inicial esperada:
   *
   * Diaz_A.pdf
   * Lagos_Diaz_A.pdf
   *
   * La interpretación se podrá ajustar después de revisar
   * los nombres reales de la empresa.
   */

  if (parts.length >= 3) {
    return {
      projectCode: parts[0],
      clientCode: parts[1],
      planTypeCode: parts[2].toUpperCase(),
      planType: getPlanTypeName_(parts[2]),
    };
  }

  if (parts.length === 2) {
    return {
      projectCode: '',
      clientCode: parts[0],
      planTypeCode: parts[1].toUpperCase(),
      planType: getPlanTypeName_(parts[1]),
    };
  }

  return {
    projectCode: '',
    clientCode: parts[0] || cleanName,
    planTypeCode: '',
    planType: 'Desconocido',
  };
}

function getPlanTypeName_(code) {
  const normalized = String(code || '')
    .trim()
    .toUpperCase();

  const types = {
    A: 'Arquitectónico',
    ARQ: 'Arquitectónico',
    E: 'Estructural',
    EST: 'Estructural',
    H: 'Hidrosanitario',
    HS: 'Hidrosanitario',
    I: 'Instalaciones',
    EL: 'Eléctrico',
    ELEC: 'Eléctrico',
    AC: 'Acabados',
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
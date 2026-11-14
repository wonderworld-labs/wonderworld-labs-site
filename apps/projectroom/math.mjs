export const FOOT = 0.3048;
export const INCH = 0.0254;
export const SQFT = FOOT ** 2;
export const CUFT = FOOT ** 3;
export const CUYD = 27 * CUFT;
export const SHORT_TON = 907.18474;

export const shapes = {
  rectangle: ['Length', 'Width'],
  triangle: ['Base', 'Perpendicular height'],
  circle: ['Diameter'],
};

export function roundUp(value) {
  // Unit conversion can put an exact whole quantity a few ulps above its integer.
  const nearest = Math.round(value);
  return Math.abs(value - nearest) <= Math.abs(value) * Number.EPSILON * 8
    ? nearest
    : Math.ceil(value);
}

export function measureArea(shape, a, b) {
  if (shape === 'circle') return Math.PI * (a / 2) ** 2;
  return a * b * (shape === 'triangle' ? 0.5 : 1);
}

export function tileQuote(area, coverage, price, delivery = 0) {
  if (![area, coverage].every(value => Number.isFinite(value) && value > 0)
      || ![price, delivery].every(value => Number.isFinite(value) && value >= 0)) return null;
  const boxes = Math.max(1, roundUp(area / coverage));
  const total = boxes * price + delivery;
  if (!Number.isSafeInteger(boxes) || !Number.isFinite(total) || total > Number.MAX_SAFE_INTEGER) return null;
  return { boxes, total };
}

export function estimate(mode, sections, settings) {
  if (!['area', 'tile', 'gravel', 'concrete'].includes(mode)) throw new Error('Unknown calculator.');
  if (!sections.some(section => !section.subtract)) throw new Error('Add at least one section to measure.');
  const volumeMode = mode === 'gravel' || mode === 'concrete';
  const positive = value => Number.isFinite(value) && value > 0;
  const nonnegative = value => Number.isFinite(value) && value >= 0;
  const rows = sections.map(({ shape, a, b, depth, subtract }, index) => {
    if (!Object.hasOwn(shapes, shape) || !positive(a) || (shape !== 'circle' && !positive(b))) {
      throw new Error(`Enter positive dimensions for section ${index + 1}.`);
    }
    if (volumeMode && !positive(depth)) throw new Error(`Enter a positive depth for section ${index + 1}.`);
    const sign = subtract ? -1 : 1;
    const area = sign * measureArea(shape, a, b);
    return { area, volume: volumeMode ? area * depth : 0 };
  });

  const area = rows.reduce((sum, row) => sum + row.area, 0);
  const volume = rows.reduce((sum, row) => sum + row.volume, 0);
  if (!positive(area)) throw new Error('Cutouts must be smaller than the total included area.');
  if (volumeMode && !positive(volume)) throw new Error('Cutouts must remove less than the total included volume.');
  if (!nonnegative(settings.waste) || settings.waste > 100) throw new Error('Enter an allowance from 0 to 100%.');
  const factor = 1 + settings.waste / 100;
  const result = { rows, area, volume, areaToBuy: area * factor, volumeToBuy: volume * factor };

  const { tileWidth, tileLength, gap, perBox, density, bagSize, bagPrice, bulkPrice } = settings;
  if (mode === 'tile') {
    if (!positive(tileWidth) || !positive(tileLength)) throw new Error('Enter positive tile dimensions.');
    if (!nonnegative(gap) || gap >= Math.min(tileWidth, tileLength)) throw new Error('Enter a grout gap smaller than both tile dimensions.');
    if (!Number.isSafeInteger(perBox) || perBox < 1) throw new Error('Enter a whole number of tiles per box.');
    result.tiles = roundUp(result.areaToBuy / ((tileWidth + gap) * (tileLength + gap)));
    result.boxes = roundUp(result.tiles / perBox);
    result.spareTiles = result.boxes * perBox - result.tiles;
  }

  if (volumeMode) {
    if (mode === 'gravel' && !positive(density)) throw new Error('Enter the supplier’s positive bulk density.');
    if (!positive(bagSize)) throw new Error('Enter the positive volume or yield printed on each bag.');
    result.weight = mode === 'gravel' ? result.volumeToBuy * density : null;
    result.bags = roundUp(result.volumeToBuy / bagSize);
    result.bagCost = bagPrice == null ? null : result.bags * bagPrice;
    result.bulkCost = bulkPrice == null ? null : result.volumeToBuy * bulkPrice;
  }

  if (['area', 'volumeToBuy', 'tiles', 'boxes', 'spareTiles', 'weight', 'bags', 'bagCost', 'bulkCost'].some(key => {
    const value = result[key];
    return value != null && (!Number.isFinite(value) || Math.abs(value) > Number.MAX_SAFE_INTEGER);
  })) throw new Error('The estimate is too large. Check your measurements and units.');
  return result;
}

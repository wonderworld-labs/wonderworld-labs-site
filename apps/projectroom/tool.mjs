import { estimate, shapes, FOOT, INCH, SQFT, CUFT, CUYD, SHORT_TON } from './math.mjs';

const root = document.querySelector('[data-tool]');
const mode = root.dataset.tool;
const isVolume = mode === 'gravel' || mode === 'concrete';
const storageKey = 'wonderworld-projectroom-v1';
const sectionList = document.querySelector('#sections');
const settingsPanel = document.querySelector('#settings');
const errorMessage = document.querySelector('#estimate-error');
const resultOutput = document.querySelector('#result-output');
const details = document.querySelector('#breakdown');
const announcer = document.querySelector('#notice');
const quickResult = document.querySelector('#quick-result');
const projectStatus = document.querySelector('#project-status');
const quickHandoff = document.querySelector('[data-handoff]');
const actionButtons = [...document.querySelectorAll('[data-output]')];
const format = new Intl.NumberFormat('en', { maximumFractionDigits: 3 });
const money = new Intl.NumberFormat('en', { maximumFractionDigits: 2, minimumFractionDigits: 2 });

const depthKey = mode === 'concrete' ? 'concreteDepth' : 'gravelDepth';
const defaultDepth = (mode === 'concrete' ? 4 : 3) * INCH;
const newSection = () => ({ shape: 'rectangle', a: null, b: null, subtract: false });
const exampleSection = () => ({ ...newSection(), a: 12 * FOOT, b: 10 * FOOT });
const sectionDepth = section => Object.hasOwn(section, depthKey)
  ? section[depthKey]
  : section.depth ?? defaultDepth;
const defaults = () => ({
  waste: mode === 'area' ? 0 : 10,
  tileWidth: 12 * INCH, tileLength: 12 * INCH, gap: 0, perBox: 10,
  density: 1.4 * SHORT_TON / CUYD, bagSize: (mode === 'concrete' ? 0.6 : 0.5) * CUFT,
  bagPrice: null, bulkPrice: null,
});
const fields = {
  waste: ['Extra material', '%'],
  tileLength: ['Tile length', 'small'],
  tileWidth: ['Tile width', 'small'],
  gap: ['Grout gap', 'small'],
  perBox: ['Tiles per box', 'tiles'],
  density: ['Bulk density', 'density'],
  bagSize: [mode === 'concrete' ? 'Mixed yield per bag' : 'Volume per bag', 'bag'],
  bagPrice: ['Price per bag (optional)', 'money'],
  bulkPrice: ['Bulk price (optional)', 'bulkPrice'],
};
const settingNames = ['waste', ...(mode === 'tile' ? ['tileLength', 'tileWidth', 'gap', 'perBox'] : []),
  ...(mode === 'gravel' ? ['density'] : []), ...(isVolume ? ['bagSize', 'bagPrice', 'bulkPrice'] : [])];
const units = {
  us: { large: ['ft', FOOT], small: ['in', INCH], area: ['ft²', SQFT], volume: ['yd³', CUYD],
    bag: ['ft³', CUFT], density: ['US ton/yd³', SHORT_TON / CUYD], weight: ['US tons', SHORT_TON],
    bulkPrice: ['per yd³', 1 / CUYD] },
  metric: { large: ['m', 1], small: ['mm', 0.001], area: ['m²', 1], volume: ['m³', 1],
    bag: ['L', 0.001], density: ['kg/m³', 1], weight: ['t', 1000], bulkPrice: ['per m³', 1] },
};
let model = { unit: 'us', sections: [newSection()], settings: {}, example: false };
try {
  const saved = JSON.parse(localStorage.getItem(storageKey));
  if (saved && Object.hasOwn(units, saved.unit) && Array.isArray(saved.sections)
      && saved.sections.length > 0 && saved.sections.length <= 25
      && saved.sections.every(row => row && Object.hasOwn(shapes, row.shape)
        && ['a', 'b', 'depth', 'concreteDepth', 'gravelDepth'].every(key =>
          row[key] == null || Number.isFinite(row[key])))) {
    model = { unit: saved.unit, sections: saved.sections, settings: saved.settings ?? {}, example: saved.example === true };
  }
} catch {}
let settings = { ...defaults(), ...model.settings[mode] };
let printText = '';

function save() {
  model.settings[mode] = settings;
  try { localStorage.setItem(storageKey, JSON.stringify(model)); } catch {}
}
function unitData(key) {
  return units[model.unit][key] || [key === 'money' ? 'amount' : key, 1];
}
function displayInput(value, key) {
  return value == null ? '' : String(Number((value / unitData(key)[1]).toPrecision(12)));
}
function valueFrom(input) {
  return input.value === '' || !Number.isFinite(input.valueAsNumber)
    ? null : input.valueAsNumber * unitData(input.dataset.unit)[1];
}
function numericField(label, key, unit, value, minimum = 0) {
  const [suffix] = unitData(unit);
  return '<label class="field"><span>' + label + '</span><span class="input-wrap"><input type="number" step="any" min="' +
    minimum + '" inputmode="decimal" data-key="' + key + '" data-unit="' + unit + '" value="' +
    displayInput(value, unit) + '"><span aria-hidden="true">' + suffix + '</span><span class="sr-only"> ' +
    suffix + '</span></span></label>';
}
function options(list, selected) {
  return Object.entries(list).map(([key, label]) =>
    '<option value="' + key + '"' + (key === selected ? ' selected' : '') + '>' + label + '</option>').join('');
}
function renderInputs() {
  document.querySelector('#units').value = model.unit;
  sectionList.innerHTML = model.sections.map((section, index) => {
    const names = shapes[section.shape];
    const multiple = model.sections.length > 1;
    return '<fieldset class="section" data-section="' + index + '"><legend>' +
      (multiple ? (section.subtract ? 'Cutout ' : 'Section ') + (index + 1) : 'Room or area') +
      '</legend><div class="measurements">' +
      numericField(names[0], 'a', 'large', section.a) +
      (names[1] ? numericField(names[1], 'b', 'large', section.b) : '') +
      (isVolume ? numericField('Depth', depthKey, 'small', sectionDepth(section)) : '') +
      '</div><div class="section-top"><label class="field"><span>Shape</span><select data-shape>' +
      options({ rectangle: 'Rectangle', triangle: 'Triangle', circle: 'Circle' }, section.shape) +
      '</select></label>' + (multiple || section.subtract
        ? '<label class="field"><span>Count as</span><select data-operation>' +
          options({ add: 'Include', subtract: 'Subtract' }, section.subtract ? 'subtract' : 'add') + '</select></label>'
        : '') + (multiple
        ? '<button type="button" class="remove" data-remove aria-label="Remove section ' +
          (index + 1) + '">&times;</button>'
        : '') + '</div></fieldset>';
  }).join('');
  settingsPanel.innerHTML = settingNames.map(key => numericField(...[fields[key][0], key, fields[key][1], settings[key]])).join('');
  document.querySelectorAll('[data-add]').forEach(button => { button.disabled = model.sections.length >= 25; });
}
function quantity(value, unit) {
  const [suffix, factor] = unitData(unit);
  const amount = value / factor;
  return (amount !== 0 && Math.abs(amount) < 0.001 ? amount.toExponential(2) : format.format(amount)) + ' ' + suffix;
}
function draw() {
  const diagram = document.querySelector('#diagram');
  const remaining = model.sections.length - 8;
  diagram.replaceChildren(...model.sections.slice(0, 8).map((section, index) => {
    const tile = document.createElement('span');
    tile.className = 'shape shape-' + section.shape + (section.subtract ? ' cutout' : '');
    tile.textContent = index + 1;
    const ratio = section.a / section.b;
    tile.style.aspectRatio = section.shape === 'circle' ? '1' : String(Math.min(2.2, Math.max(0.65, ratio || 1)));
    return tile;
  }));
  const caption = document.querySelector('#diagram-caption');
  caption.textContent = 'Section sketches, shown individually' + (remaining > 0 ? ' · +' + remaining + ' more' : '');
}
function fillList(list, pairs) {
  list.replaceChildren(...pairs.flatMap(([label, value]) => {
    const name = document.createElement('dt');
    const amount = document.createElement('dd');
    name.textContent = label;
    amount.textContent = value;
    return [name, amount];
  }));
}
function update() {
  save();
  projectStatus.textContent = model.example ? 'Example measurements' : '';
  let result;
  try {
    for (const key of ['bagPrice', 'bulkPrice']) {
      if (isVolume && settings[key] != null && settings[key] < 0) throw new Error('Enter a price of zero or more.');
    }
    const sections = isVolume ? model.sections.map(section => ({ ...section, depth: sectionDepth(section) })) : model.sections;
    result = estimate(mode, sections, settings);
  } catch (error) {
    const empty = model.sections.length === 1 && model.sections[0].a == null && model.sections[0].b == null;
    errorMessage.textContent = empty ? 'Enter your measurements to see an estimate.' : error.message;
    quickResult.textContent = errorMessage.textContent;
    errorMessage.hidden = false;
    resultOutput.hidden = true;
    details.hidden = true;
    if (quickHandoff) quickHandoff.hidden = true;
    actionButtons.forEach(button => { button.disabled = true; });
    return;
  }
  errorMessage.hidden = true;
  resultOutput.hidden = false;
  if (quickHandoff) quickHandoff.hidden = false;
  details.hidden = result.rows.length === 1;
  if (!details.hidden) draw();
  actionButtons.forEach(button => { button.disabled = false; });

  let main = ['Net area', quantity(result.area, 'area')];
  const rows = [];
  if (mode === 'area' || mode === 'tile') {
    const alternate = model.unit === 'us' ? 'metric' : 'us';
    const [label, factor] = units[alternate].area;
    if (mode === 'tile') rows.push(['Net area', quantity(result.area, 'area')]);
    rows.push(['Equivalent area', format.format(result.area / factor) + ' ' + label]);
    if (settings.waste > 0) rows.push(['Area with allowance', quantity(result.areaToBuy, 'area')]);
  }
  if (mode === 'tile') {
    main = ['Boxes to buy', format.format(result.boxes) + (result.boxes === 1 ? ' box' : ' boxes')];
    rows.push(['Tiles needed', format.format(result.tiles)], ['Extra tiles from whole boxes', format.format(result.spareTiles)]);
  }
  if (isVolume) {
    main = ['Volume to order', quantity(result.volumeToBuy, 'volume')];
    rows.push(['Volume before allowance', quantity(result.volume, 'volume')], ['Order volume in ' + unitData('bag')[0], quantity(result.volumeToBuy, 'bag')],
      ['Whole bags', format.format(result.bags)]);
    if (result.weight != null) rows.push(['Estimated bulk weight', quantity(result.weight, 'weight')]);
    if (result.bagCost != null) rows.push(['Bagged material cost', money.format(result.bagCost)]);
    if (result.bulkCost != null) rows.push(['Bulk material cost', money.format(result.bulkCost)]);
  }
  document.querySelector('#result-label').textContent = main[0];
  document.querySelector('#total').textContent = main[1];
  quickResult.textContent = main[0] + ': ' + main[1];
  fillList(document.querySelector('#totals'), rows);
  const parts = result.rows.map((row, index) => [
    (model.sections[index].subtract ? 'Cutout ' : 'Section ') + (index + 1),
    quantity(row.area, 'area') + (isVolume ? ' · ' + quantity(row.volume, 'volume') : ''),
  ]);
  fillList(document.querySelector('#section-totals'), parts);
  printText = [document.title.split(' | ')[0], ...[main, ...rows, ...parts].map(pair => pair.join(': '))].join('\n');
}

document.querySelector('#units').addEventListener('change', event => {
  model.unit = event.target.value;
  renderInputs();
  update();
});
root.addEventListener('input', event => {
  const input = event.target;
  if (!input.matches('input[data-key]')) return;
  const group = input.closest('[data-section]');
  const target = group ? model.sections[Number(group.dataset.section)] : settings;
  target[input.dataset.key] = valueFrom(input);
  input.setAttribute('aria-invalid', String(input.validity.badInput || input.validity.rangeUnderflow));
  update();
});
sectionList.addEventListener('change', event => {
  const input = event.target;
  if (!input.matches('select')) return;
  const index = Number(input.closest('[data-section]').dataset.section);
  if (input.hasAttribute('data-shape')) model.sections[index].shape = input.value;
  else model.sections[index].subtract = input.value === 'subtract';
  const selector = input.hasAttribute('data-shape') ? '[data-shape]' : '[data-operation]';
  renderInputs();
  sectionList.querySelector('[data-section="' + index + '"] ' + selector).focus();
  update();
});
root.addEventListener('click', async event => {
  const button = event.target.closest('button');
  if (!button) return;
  if (button.hasAttribute('data-add')) {
    const subtract = button.dataset.add === 'cutout';
    const section = { ...newSection(), subtract };
    if (isVolume) section[depthKey] = sectionDepth(model.sections[0]) ?? defaultDepth;
    model.sections.push(section);
    renderInputs();
    sectionList.lastElementChild.querySelector('input').focus();
    update();
  }
  if (button.hasAttribute('data-remove')) {
    const index = Number(button.closest('[data-section]').dataset.section);
    model.sections.splice(index, 1);
    renderInputs();
    sectionList.children[Math.min(index, model.sections.length - 1)].querySelector('select').focus();
    update();
  }
  if (button.hasAttribute('data-sample') || button.hasAttribute('data-clear')) {
    model.example = button.hasAttribute('data-sample');
    model.sections = [model.example ? exampleSection() : newSection()];
    settings = defaults();
    renderInputs();
    update();
    sectionList.querySelector('input').focus();
    announcer.textContent = model.example ? 'Example loaded.' : 'Measurements cleared.';
  }
  if (button.dataset.output === 'print') window.print();
  if (button.dataset.output === 'copy') {
    try {
      await navigator.clipboard.writeText(printText);
      announcer.textContent = 'Estimate copied.';
    } catch {
      const text = document.querySelector('#copy-fallback');
      text.hidden = false;
      text.value = printText;
      text.focus();
      text.select();
      announcer.textContent = 'Select and copy the estimate below.';
    }
  }
});
document.querySelector('#copy-fallback').addEventListener('blur', event => { event.target.hidden = true; });

renderInputs();
update();

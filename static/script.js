const form = document.getElementsByTagName("form")[0];
const addSeriesResistorButton = document.getElementById(
  "add-series-resistor-button"
);
const addParallelResistorButton = document.getElementById(
  "add-parallel-resistor-button"
);

let seriesIndex = 0;
const resistors = [];

const resistor = {
  outerIndex: 0,
  innerIndex: 10,
  valueOhms: 400,
};

const addSeriesResistorField = () => {
  const setResistorTypeSeries = (resistor) => {
    resistor.className = "resistor series";
    resistor.name = `R${resistors.length} ${seriesIndex} Series`;
    resistor.value = 10;
  };
  if (checkChangeInResistorType("Series")) seriesIndex++;
  const newField = createResistorField();
  setResistorTypeSeries(newField);
  resistors.push(newField);
  addSeriesResistorButton.before(newField);
};

const addParallelResistorField = () => {
  const setResistorTypeParallel = (resistor) => {
    resistor.className = "resistor parallel";
    resistor.name = `R${resistors.length} ${seriesIndex} Parallel`;
    resistor.value = 10;
  };
  if (checkChangeInResistorType("Parallel")) seriesIndex++;
  const newField = createResistorField();
  setResistorTypeParallel(newField);
  // Overwrite previous field to become Parallel as well
  const lastField = resistors.pop();
  if (lastField.name.includes("Series")) setResistorTypeParallel(lastField);
  resistors.push(lastField);
  resistors.push(newField);
  addSeriesResistorButton.before(newField);
};

const createResistorField = () => {
  const input = document.createElement("input");
  input.type = "text";
  return input;
};

const checkChangeInResistorType = (newFieldType) => {
  const lastField = resistors[resistors.length - 1];
  if (
    lastField != undefined &&
    lastField.name.split(" ").pop() !== newFieldType
  )
    return true;
  else return false;
};

const checkEmptyFields = () => {
  const inputElements = document.getElementsByTagName("input");
  for (const element of inputElements) if (element.value === "") return false;
  return true;
};

const submit = (e) => {
  e.preventDefault();
  if (!checkEmptyFields()) return false;
  const formData = new FormData(form);
  const data = {};
  formData.forEach((k, v) => {
    data[k] = v;
  });
  const json = JSON.stringify(data);
  return true;
};

addSeriesResistorField();
addSeriesResistorButton.onclick = addSeriesResistorField;
addParallelResistorButton.onclick = addParallelResistorField;
form.onsubmit = submit;

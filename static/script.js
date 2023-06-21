const form = document.querySelector("form");
const voltageField = document.getElementById("voltage-field");
const outerList = document.querySelector("ul");
const addResistorBtn = document.getElementById("add-resistor-btn");
const pierceChbx = document.getElementById("pierce");
const stepBackBtn = document.getElementById("step-back-btn");

let project = { components: [] };
let head = outerList;
let count = 0;

const createResistor = (type) => {
  const resistor = document.createElement("li");
  const inputField = document.createElement("input");
  inputField.type = "number";
  resistor.appendChild(inputField);
  resistor.dataset.type = type;
  resistor.dataset.name = "R" + count++;
  return resistor;
};

const addResistor = () => {
  const inputs = [
    ...document.getElementById("controls").getElementsByTagName("input"),
  ];
  mode = inputs.filter((input) => input.type === "radio" && input.checked)[0]
    .id;
  const resistor = createResistor(mode);
  if (mode === "parallel") {
    if (pierceChbx.value === "on") {
      const wrapper = document.createElement("li");
    }

    const newList = document.createElement("ul");
    head.appendChild(wrapper.appendChild(newList));
    head = newList;
    console.log(head);
  }
  head.appendChild(resistor);
};

const stepBack = () => {
  if (head.parentElement.tagName !== "FORM") head = head.parentElement;
  console.log("HEAD ", head);
};

const submit = (e) => {
  e.preventDefault();
  children = [...outerList.children];
  project.voltage = children.shift().firstElementChild.value;
  console.log(project);

  // const addSeriesData = (list) => {};

  // const addParallelData = (list) => {
  //   branches = [];
  //   for (const item of [...list.children]) {
  //     branches.push({
  //       name: item.dataset.name,
  //       resistance: item.firstElementChild.value,
  //     });
  //   }
  //   project.components.push({
  //     type: "Parallel",
  //     branches: branches,
  //   });
  // };

  // for (const child of [...outerList.children]) {
  //   input = child.firstElementChild;
  //   if (child.tagName === "LI") {
  //     project.components.push({
  //       type: "Series",
  //       resistor: {
  //         name: child.dataset.name,
  //         resistance: input.value,
  //       },
  //     });
  //   } else if (child.tagName === "UL") {
  //     addParallelData(child);
  //   }
  // }
  // console.log(project);
};

const save = () => {};
const load = () => {};

form.onsubmit = submit;
addResistorBtn.onclick = addResistor;
stepBackBtn.onclick = stepBack;

const outerList = document.querySelector("ul");
const stepFwdChbx = document.getElementById("step-fwd-chbx");

let project = {};
let head = undefined;
let count = 0;

const moveHead = (newHead) => {
  if (head != undefined) head.dataset.isHead = false;
  newHead.dataset.isHead = true;
  head = newHead;
};
moveHead(outerList);

const createResistor = () => {
  const inputField = document.createElement("input");
  inputField.type = "number";
  inputField.required = true;
  inputField.placeholder = `R${count}`;
  inputField.dataset.name = `R${count++}`;
  return inputField;
};

const addResistor = () => {
  const type = [
    ...document.getElementById("controls").getElementsByTagName("input"),
  ].filter((input) => input.type === "radio" && input.checked)[0].id;

  const component = document.createElement("li");
  if (type === "series") {
    if (head.tagName === "LI") {
      const newList = document.createElement("ul");
      head.appendChild(newList);
      moveHead(newList);
      console.log(head);
    }
    component.dataset.type = type;
    component.appendChild(createResistor());
    head.appendChild(component);
  } else if (type === "parallel") {
    if (stepFwdChbx.checked) {
      if (head.tagName !== "UL") {
        alert("Can't Step Further");
        stepFwdChbx.checked = false;
        return;
      }
      const wrapper = document.createElement("li");
      wrapper.className = "parallel-wrapper";
      wrapper.dataset.type = type;
      head.appendChild(wrapper);
      moveHead(wrapper);
      console.log(head);
    } else {
      if (head.tagName !== "LI") {
        alert("Step Forward");
        return;
      }
    }
    head.appendChild(createResistor());
    stepFwdChbx.checked = false;
  }
};

const stepBack = () => {
  const headTag = head.parentElement.tagName;
  if (headTag !== "FORM" && headTag !== "DIV") moveHead(head.parentElement);
  console.log("HEAD ", head);
};

const submit = (e) => {
  e.preventDefault();
  const children = [...outerList.children];
  project.voltage = children.shift().firstElementChild.value;
  project.components = encode(children);
  console.log("Post Body: ", project);
  fetch("/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(project),
  })
    .then((response) => response.text())
    .then((html) => (document.querySelector("html").innerHTML = html));
};

const encode = (componentList) => {
  const components = [];
  for (const component of componentList) {
    const type = component.dataset.type;
    if (type === "series") newData = addSeriesData(component);
    else if (type === "parallel") newData = addParallelData(component);
    else throw new Error("Invalid Component Type");
    components.push(newData);
  }
  console.log("Componenets:", components);
  return components;
};

const addSeriesData = (component) => {
  const inputField = component.firstElementChild;
  return {
    type: "Series",
    resistor: {
      name: inputField.dataset.name,
      resistance: inputField.value,
    },
  };
};

const addParallelData = (component) => {
  const branches = [...component.children];
  const branchList = [];
  for (const branch of branches) {
    // Component List
    if (branch.tagName === "UL") {
      aaa = encode([...branch.children]);
      console.log("Branch Children: ", [...branch.children], aaa);
      branchList.push(aaa);
      continue;
    }
    console.log(branches);
    console.log(branch);
    inputField = branch;
    branchList.push({
      name: inputField.dataset.name,
      resistance: inputField.value,
    });
  }
  return {
    type: "Parallel",
    branches: branchList,
  };
};

document.querySelector("form").onsubmit = submit;
document.getElementById("add-resistor-btn").onclick = addResistor;
document.getElementById("step-back-btn").onclick = stepBack;

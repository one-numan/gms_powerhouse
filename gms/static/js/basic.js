var js_data = {
  Name: "",
  Email: "",
  "Total Subject": "",
  "Subject Data": [],
  "Total Gain": "",
  "Total Marks": "",
  "Total Loss": "",
  "Total Percentage": "",
};

const s2formMarks = document.getElementById("formMarks");

var counttotalSubject = 0;
let final_Subject_Name = [],
  final_Subject_Marks = [],
  final_Subject_Gain = [],
  final_Subject_Percentage = [],
  final_Subject_Loss = [];

let step1 = document.getElementById("step1");
let step2 = document.getElementById("step2");
let step3 = document.getElementById("step3");
let ls = localStorage;
// console.log(ls);

function marksPercentage(percentage_value) {
  document.getElementById("info_marksPercentage").innerText =
    percentage_value.toFixed(3);
  new ApexCharts(document.querySelector("#marksPercentage"), {
    series: [percentage_value],
    chart: {
      height: 350,
      type: "radialBar",
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 225,
        hollow: {
          margin: 0,
          size: "50%",
          background: "#fff",
          image: undefined,
          imageOffsetX: 0,
          imageOffsetY: 0,
          position: "front",
          dropShadow: {
            enabled: true,
            top: 3,
            left: 0,
            blur: 4,
            opacity: 0.24,
          },
        },
        track: {
          background: "#fff",
          strokeWidth: "67%",
          margin: 0, // margin is in pixels
          dropShadow: {
            enabled: true,
            top: -3,
            left: 0,
            blur: 4,
            opacity: 0.35,
          },
        },

        dataLabels: {
          show: true,
          name: {
            offsetY: -10,
            show: true,
            color: "#888",
            fontSize: "17px",
          },
          value: {
            formatter: function (val) {
              return parseInt(val);
            },
            color: "#111",
            fontSize: "36px",
            show: true,
          },
        },
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        shade: "dark",
        type: "horizontal",
        shadeIntensity: 0.5,
        gradientToColors: ["#ABE5A1"],
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100],
      },
    },
    stroke: {
      lineCap: "round",
    },
    labels: ["Percent"],
  }).render();
}

function markSubjecWise(all_subject_name, all_subject_marks) {
  document.getElementById("info_donutChart").innerText =
    all_subject_marks[1] + " and " + all_subject_marks[0];
  new ApexCharts(document.querySelector("#donutChart"), {
    series: all_subject_marks,
    chart: {
      width: "100%",
      type: "pie",
      height: 250,

      toolbar: {
        show: false,
      },
      dataLabels: {
        show: true,
      },
    },
    labels: all_subject_name,
    theme: {
      monochrome: {
        enabled: false,
      },
    },
  }).render();
}

function buildBarChart2(subjectMarks, SubjectNames) {
  let grade_a = [],
    grade_b = [],
    grade_c = [],
    grade_d = [];
  for (let index1 = 0; index1 < subjectMarks.length; index1++) {
    grade_a.push(90);
    grade_b.push(70);
    grade_c.push(60);
    grade_d.push(50);
  }
  // console.log(subjectMarks);
  new ApexCharts(document.querySelector("#buildBarChart2"), {
    series: [
      {
        name: "Marks",
        type: "column",
        data: subjectMarks,
      },
      {
        name: "A+ Grade",
        type: "line",
        data: grade_a,
      },
      {
        name: "B Grade",
        type: "line",
        data: grade_b,
      },
      {
        name: "C Grade",
        type: "line",
        data: grade_c,
      },
      {
        name: "D Grade",
        type: "line",
        data: grade_d,
      },
    ],
    chart: {
      height: 350,
      type: "line",
      stacked: false,
    },
    stroke: {
      width: 4,
      curve: "smooth",
    },
    plotOptions: {
      bar: {
        columnWidth: "10%",
      },
    },

    fill: {
      opacity: [0.85, 0.25, 1],
      gradient: {
        inverseColors: false,
        shade: "light",
        type: "vertical",
        opacityFrom: 0.85,
        opacityTo: 0.55,
        stops: [0, 100, 100, 100],
      },
    },
    labels: SubjectNames,
    markers: {
      size: 0,
    },
    xaxis: {
      title: {
        text: "Subjects",
        position: "bottom",
      },
    },
    yaxis: {
      title: {
        text: "Percentage",
      },
      min: 0,
    },
    toolbar: {
      show: false,
    },
    tooltip: {
      shared: false,
      intersect: true,
      y: {
        formatter: function (y) {
          if (typeof y !== "undefined") {
            return y.toFixed(0) + " Percent";
          }
          return y;
        },
      },
    },
  }).render();
}

// function buildBarCharts() {
//   console.log("Function Calling");
//   new ApexCharts(document.querySelector("#buildBarCharts"), {
//     series: [
//       {
//         data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380],
//       },
//     ],
//     chart: {
//       type: "bar",
//       height: 350,
//     },
//     plotOptions: {
//       bar: {
//         borderRadius: 4,
//         horizontal: true,
//       },
//     },
//     dataLabels: {
//       enabled: false,
//     },
//     xaxis: {
//       categories: [
//         "South Korea",
//         "Canada",
//         "United Kingdom",
//         "Netherlands",
//         "Italy",
//         "France",
//         "Japan",
//         "United States",
//         "China",
//         "Germany",
//       ],
//     },
//   }).render();
//   console.log("Function Calling");
// }

function createTrField(js_data) {
  // console.log(js_data);
  for (let element of js_data["Subject Data"]) {
    let subjectPercentage = element["Subject Percentage"].toFixed(3);

    let backgroundColor = "table-danger";
    // console.log(subjectPercentage >= 90.0);
    let performance = "Fail";
    if (subjectPercentage >= 90.0) {
      backgroundColor = "table-primary";
      performance = "Excellent";
    } else if (subjectPercentage >= 80.0) {
      backgroundColor = "table-info";
      performance = "Very Good";
    } else if (subjectPercentage >= 70.0) {
      backgroundColor = "table-success";
      performance = "Good";
    } else if (subjectPercentage >= 60.0) {
      performance = "Average";
      backgroundColor = "table-warning";
    } else if (subjectPercentage >= 50.0) {
      performance = "Poor";
      backgroundColor = "table-dark";
    }
    subjectMarksHTML = `
            <tr class= ${backgroundColor}>
            <th scope="row">${element["Subject Name"]}</th>
            <td>${element["Subject Marks"]}</td>
            <td>${element["Subject Gain"]}</td>
            
            <td>${subjectPercentage}</td>
            <td>${performance}</td>
          </tr>`;

    document.getElementById("tbodySubject").innerHTML += subjectMarksHTML;
  }
}
function createMarksField(subjectId) {
  // console.log("Enter The Subject ID", subjectId);
  let subjectMarksHTML = `
      <hr>
    <b>Subject ${subjectId + 1} Detail</b>
    <div class="row mb-3 mt-2">
      <label for="inputText" class="col-sm-2 col-form-label">Name</label>
      <div class="col-sm-10">
        <input type="text" maxlength="14" min="3" class="form-control"  id="subjectId${subjectId}" placeholder="Subject Name ${
    subjectId + 1
  } " required>
  
  </div>
  </div>
  <div class="row mb-3">
  <label for="inputEmail" class="col-sm-2 col-form-label">Total Marks</label>
  <div class="col-sm-10">
  <input type="number" max=100 min=1 class="form-control"  id="subjectTM${subjectId}" placeholder="Subject ${
    subjectId + 1
  }  Total Marks  " required>
  </div>
  </div>
  <div class="row mb-3">
  <label for="inputEmail" class="col-sm-2 col-form-label">Gain Marks</label>
  <div class="col-sm-10">
  <input type="number"  min=0 class="form-control"  id="subjectGM${subjectId}" placeholder="Subject ${
    subjectId + 1
  } Gain Marks ${subjectId + 1} " required>
  <div id="subjectValidate${subjectId}" class="form-text text-danger d-none"><b>Wrong Input</b></div>
  </div>
  </div>
  `;
  // Append the subject marks HTML code to the DOM
  document.getElementById("formMarks").innerHTML += subjectMarksHTML;
}

const divMarks = document.getElementById("divMarks");
const formMarks = document.getElementById("formMarks");

function checkValidation() {
  // console.log(counttotalSubject);
  let validate = false;
  for (let index = 0; index < counttotalSubject; index++) {
    // console.log("Click It", counttotalSubject);
    let this_subject_marks = parseInt(s2formMarks["subjectTM" + index].value);
    let this_subject_gain = parseInt(s2formMarks["subjectGM" + index].value);

    if (this_subject_marks < this_subject_gain) {
      validate = true;
      // console.log("False");
      document
        .getElementById("subjectValidate" + index)
        .classList.remove("d-none");
      // console.log("S2");
    } else {
      document
        .getElementById("subjectValidate" + index)
        .classList.add("d-none");
    }
  }
  return validate;
}

// Main Function

// Create a variable that hold form Data
const formSubject = document.getElementById("formSubject");
formSubject.addEventListener("submit", (e) => {
  e.preventDefault();

  // console.log("Form Submitted");
  // console.log(
  //   formSubject.studentEmail.value,
  //   formSubject.studentName.value,
  //   formSubject.studentSubject.value
  // );
  js_data.Email = formSubject.studentEmail.value;
  js_data.Name = formSubject.studentName.value;
  js_data["Total Subject"] = formSubject.studentSubject.value;
  // console.log(js_data);

  // Step 1
  // Change Submit btn Color , Name
  submitS1Btn = document.getElementById("submitS1Btn");
  submitS1Btn.style.display = "none";
  // submitS1Btn.classList.add("btn-success");

  // submitS1Btn.innerHTML = '<i class="bi bi-arrow-down"></i>';
  // submitS1Btn.type = "button";

  document.getElementById("down-btn").classList.remove("d-none");

  // Remove input btn
  formSubject.resetS1Btn.style.display = "none";

  //ReadOnly Text Field
  formSubject.studentEmail.readOnly = "true";
  formSubject.studentName.readOnly = "true";
  formSubject.studentSubject.readOnly = "true";

  // Display the block True
  divMarks.style.display = "block";

  // Step 1 Process Green Box
  step1.classList.remove("active");
  step1.classList.add("completed");
  step2.classList.add("active");

  // Create Input Field for Subject
  const totalSubject = parseInt(formSubject.studentSubject.value);
  counttotalSubject = totalSubject;
  for (let index = 0; index < totalSubject; index++) {
    // console.log(index);
    createMarksField(index);
  }
  // insert Submited Btn
  let subjectSubmitBtn = `<button type="submit" class="btn btn-primary rounded-0" id="submitSubject" >Generate Report</button> <p id="submitSubjectHint"></p>`;
  document.getElementById("formMarks").innerHTML += subjectSubmitBtn;

  window.scrollTo(0, divMarks.offsetTop);
});

// Step 2
s2formMarks.addEventListener("submit", (e) => {
  e.preventDefault();
  if (checkValidation()) {
    document.getElementById("submitSubjectHint").innerText =
      "Oh! You Insert Wrong Input";
    return true;
  }
  document.getElementById("submitSubjectHint").innerText = "";
  // console.log("2nd Form Submitted");
  // Step 1 Process Green Box
  step2.classList.remove("active");
  step2.classList.add("completed");
  step3.classList.add("completed");

  // console.log(counttotalSubject);
  let sumTotalMarks = 0;
  let sumGainMarks = 0;
  let sumLossMarks = 0;

  for (let index = 0; index < counttotalSubject; index++) {
    // console.log("Name Of Subject", s2formMarks["subjectId" + index].value);

    // console.log("Total Marks", s2formMarks["subjectTM" + index].value);
    let this_subject_marks = parseInt(s2formMarks["subjectTM" + index].value);
    let this_subject_gain = parseInt(s2formMarks["subjectGM" + index].value);
    let this_subject_loss =
      parseInt(s2formMarks["subjectTM" + index].value) -
      parseInt(s2formMarks["subjectGM" + index].value);

    sumTotalMarks = this_subject_marks + sumTotalMarks;
    sumGainMarks = this_subject_gain + sumGainMarks;
    sumLossMarks = this_subject_loss + sumLossMarks;

    // console.log("Gain Marks", s2formMarks["subjectGM" + index].value);
    js_data["Subject Data"].push({
      "Subject Name": s2formMarks["subjectId" + index].value,
      "Subject No": index + 1,
      "Subject Marks": this_subject_marks,
      "Subject Gain": this_subject_gain,
      "Subject Loss": this_subject_loss,
      "Subject Percentage": (this_subject_gain / this_subject_marks) * 100,
    });
    // console.log(js_data);
  }
  js_data["Total Loss"] = sumLossMarks;
  js_data["Total Gain"] = sumGainMarks;
  js_data["Total Marks"] = sumTotalMarks;
  js_data["Total Percentage"] = (sumGainMarks / sumTotalMarks) * 100;

  for (let element of js_data["Subject Data"]) {
    final_Subject_Percentage.push(parseInt(element["Subject Percentage"]));
    final_Subject_Name.push(element["Subject Name"]);
    final_Subject_Marks.push(element["Subject Marks"]);
    final_Subject_Gain.push(element["Subject Gain"]);
    final_Subject_Loss.push(element["Subject Loss"]);
  }

  document.getElementById("tableName").innerText = js_data["Name"];
  document.getElementById("tableEmail").innerText = js_data["Email"];
  document.getElementById("tableTotalSubject").innerText =
    js_data["Total Subject"];

  let today = new Date();
  let formattedDate = today.toISOString().replace("T", " ").substring(0, 19);

  js_data["time"] = formattedDate;

  createTrField(js_data);

  // Encrypt the JSON object
  let encryptedObject = btoa(JSON.stringify(js_data));
  console.log("Encrypted");
  if (ls.length <= 5) {
    console.log("Condition True");
    ls.setItem(formattedDate, encryptedObject);
  } else {
    let l_keys = Object.keys(localStorage).sort();
    console.log("Condition False");
    for (let i = ls.length; i >= 4; i--) {
      let min_key = l_keys[i];
      console.log("Removing");
      localStorage.removeItem(min_key);
    }
    // console.log(min_key);
    ls.setItem(formattedDate, encryptedObject);
  }

  // Report Table Div Enable
  const divTable = (document.getElementById("divTable").style.display =
    "Block");

  // Chart 1
  // console.log("final_Subject_Percentage", final_Subject_Percentage);
  document.getElementById("divChart1").style.display = "block";
  marksPercentage(js_data["Total Percentage"]);

  // Chart 2
  document.getElementById("divChart2").style.display = "block";

  markSubjecWise(
    ["Loss", "Gain"],
    [js_data["Total Loss"], js_data["Total Gain"]]
  );

  document.getElementById("divChart3").style.display = "block";
  buildBarChart2(final_Subject_Percentage, final_Subject_Name);

  // buildBarCharts();

  // console.log(sumTotalMarks);
  // document.getElementById("TextSumTotalMarks").innerHTML =
  //   "Total Marks" + sumTotalMarks + " " + sumGainMarks + " are ";
  divMarks.style.display = "none";
  document.getElementById("divDetail").style.display = "none";

  // console.log("js_data", js_data["Subject Data"]);
  window.scrollTo(0, divTable.offsetTop);
  showFeedback();
});
// console.clear();

function history_fetch() {
  let all_ls = localStorage;
  // console.log(all_ls);
  if (all_ls.length === 0) {
    let history_data = `<li>
    <hr class="dropdown-divider">
    </li>
    <li class="notification-item">
    <i class="bi bi-check-circle text-success"></i>
    <div>
        <h4>No History Found</h4>
        <p>Oh! Your Still Not Generate Result</p>
        
    </div>
    </li>`;
    document.getElementById("history-section").innerHTML += history_data;
  } else {
    for (let index = 0; index < all_ls.length; index++) {
      //   element = all_ls[index];
      // console.log(all_ls[index]);
      let l_keys = Object.keys(localStorage).sort();
      // console.log(l_keys[index]);
      let encryptedObject = localStorage.getItem(l_keys[index]);
      // console.log(encryptedObject);
      // Decrypt the JSON object
      let en_data = JSON.parse(atob(encryptedObject));
      // console.log(en_data);
      let history_data = `            <li>
    <hr class="dropdown-divider">
    </li>

    <li>
    <hr class="dropdown-divider">
    </li>
    <li class="notification-item">
    <i class="bi bi-check-circle text-success"></i>
    <div>
        <h4>${en_data["Name"]} </h4>
        <h6>Your Gain Total Percentage ${en_data["Total Percentage"].toFixed(
          3
        )}</h6>
        <p>${en_data["time"]}</p>
    </div>
    </li>

    <li>
    <hr class="dropdown-divider">
    </li>`;

      document.getElementById("history-section").innerHTML += history_data;

      if (index === 5) {
        break;
      }
    }
    let reloadBtn = `<li class="dropdown-footer">
    <a href="#" onclick='windowReload()'>Reload</a>
    </li>`;
    document.getElementById("history-section").innerHTML += reloadBtn;
  }
}

function clearhistory() {
  localStorage.clear();
  windowReload();
}
history_fetch();

function windowReload() {
  window.location.reload();
}

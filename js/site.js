(function () {
  document.querySelectorAll("[data-faq]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = btn.nextElementSibling;
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      if (panel) panel.hidden = open;
    });
  });

  var form = document.querySelector("#estimate-form");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = new FormData(form);
    var result = document.querySelector("#estimate-result");
    var lines = [
      "지역: " + (data.get("area") || ""),
      "서비스: " + (data.get("service") || ""),
      "연락처: " + (data.get("phone") || ""),
      "내용: " + (data.get("memo") || "전화로 말씀드리겠습니다.")
    ];
    result.hidden = false;
    result.innerHTML = "";
    var title = document.createElement("strong");
    title.textContent = "상담 신청 내용입니다. 아래 번호로 전화하시면 이어서 안내드립니다.";
    var p = document.createElement("p");
    p.textContent = lines.join("\n");
    p.style.whiteSpace = "pre-line";
    result.appendChild(title);
    result.appendChild(p);
    var link = document.createElement("a");
    link.href = form.getAttribute("data-tel");
    link.textContent = "전화 연결 " + form.getAttribute("data-phone");
    result.appendChild(link);
  });
})();

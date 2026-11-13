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

  var PUBLIC_KEY = "JKsVOKPtnWHIr2BCV";
  var SERVICE_ID = "allbarunclean";
  var TEMPLATE_ID = "template_b4ox5js";

  function loadEmailJs() {
    if (window.emailjs) return Promise.resolve();
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js";
      script.onload = function () { resolve(); };
      script.onerror = function () { reject(new Error("emailjs")); };
      document.head.appendChild(script);
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var data = new FormData(form);
    var result = document.querySelector("#estimate-result");
    var button = form.querySelector("button[type='submit']");
    var area = data.get("area") || "";
    var service = data.get("service") || "";
    var phone = data.get("phone") || "";
    var memo = data.get("memo") || "전화로 말씀드리겠습니다.";
    var page = location.href;
    var body = [
      "[무브투헤븐 상담 신청]",
      "",
      "사이트: heaven.allbarunclean.com",
      "페이지: " + page,
      "지역: " + area,
      "서비스: " + service,
      "연락처: " + phone,
      "내용: " + memo
    ].join("\n");

    if (button) {
      button.disabled = true;
      button.textContent = "전송 중...";
    }
    result.hidden = false;
    result.textContent = "상담 내용을 보내는 중입니다.";

    loadEmailJs()
      .then(function () {
        emailjs.init({ publicKey: PUBLIC_KEY });
        return emailjs.send(SERVICE_ID, TEMPLATE_ID, {
          from_name: "무브투헤븐",
          name: "무브투헤븐",
          phone: phone,
          region: area,
          service: "무브투헤븐 / " + service,
          message: body
        });
      })
      .then(function () {
        result.innerHTML = "";
        var title = document.createElement("strong");
        title.textContent = "상담 신청이 접수되었습니다. 확인 후 연락드립니다.";
        var p = document.createElement("p");
        p.style.whiteSpace = "pre-line";
        p.textContent = ["지역: " + area, "서비스: " + service, "연락처: " + phone, "내용: " + memo].join("\n");
        var link = document.createElement("a");
        link.href = form.getAttribute("data-tel");
        link.textContent = "전화 연결 " + form.getAttribute("data-phone");
        result.appendChild(title);
        result.appendChild(p);
        result.appendChild(link);
        form.reset();
      })
      .catch(function () {
        result.innerHTML = "";
        var title = document.createElement("strong");
        title.textContent = "메일 전송에 실패했습니다. 아래 번호로 전화해 주세요.";
        var link = document.createElement("a");
        link.href = form.getAttribute("data-tel");
        link.textContent = "전화 연결 " + form.getAttribute("data-phone");
        result.appendChild(title);
        result.appendChild(link);
      })
      .finally(function () {
        if (button) {
          button.disabled = false;
          button.textContent = "빠른 상담 신청하기";
        }
      });
  });
})();

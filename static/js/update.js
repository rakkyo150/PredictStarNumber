$(function () {
    $.ajax({
        url: "/init",
        type: "post",
        data: "読み込み開始",
    })
        .done(function (data) {
            $("div.nowLoading").css("display", "none");
            $("div.finishLoading").css("display", "block");
        })
        .fail(function () {
            $("div.nowLoading").css("display", "none");
            $("div.errorLoading").css("display", "block");
        });

    $("input.submit").click(function () {
        const checkValue = $('input:radio[name="mode"]:checked').val();
        const postData = { mode: checkValue, input: $("input.input").val() };

        $.ajax({
            url: "/predict",
            type: "post",
            data: postData,
        })
            .done(function (data) {
                let resultHtml = "";

                let jsonData = {};
                data.forEach(function (item) {
                    jsonData[item[0]] = item[1];
                });

                Object.keys(jsonData).forEach(function (key) {
                    resultHtml += `<p>${key} : ${jsonData[key]}</p>\n`;
                }, data);
                $("h1.resultMain").html(resultHtml);
                $("div.errorPredict").css("display", "none");
                $("div.finishPredict").css("display", "block");
            })
            .fail(function () {
                $("h1.errorSentence").text("Your input is OK?");
                $("div.finishPredict").css("display", "none");
                $("div.errorPredict").css("display", "block");
            });
    });
});

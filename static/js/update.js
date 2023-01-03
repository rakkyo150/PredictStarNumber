$(function () {
    $.ajax({
        url: "/init",
        type: "post",
        data: "読み込み開始",
    })
        .done(function (data) {
            console.log(data);
            $("div.nowLoading").css("display", "none");
            $("div.finishLoading").css("display", "block");
        })
        .fail(function () {
            console.log("Failed to load");
            $("div.nowLoading").css("display", "none");
            $("div.errorLoading").css("display", "block");
        });

    $("input.submit").click(function () {
        console.log("checkValue");
        const checkValue = $('input:radio[name="mode"]:checked').val();
        console.log(checkValue);

        console.log("postData");
        const postData = { mode: checkValue, input: $("input.input").val() };

        $.ajax({
            url: "/predict",
            type: "post",
            data: postData,
        })
            .done(function (data) {
                let resultHtml = "";
                console.log(data);
                Object.keys(data).forEach(function (key) {
                    resultHtml += `<p>${key} : ${this[key]}</p>\n`;
                }, data);
                $("h1.resultMain").html(resultHtml);
                $("div.errorPredict").css("display", "none");
                $("div.finishPredict").css("display", "block");
            })
            .fail(function () {
                console.log("Failed to predict");
                $("h1.errorSentence").text("Your input is OK?");
                $("div.finishPredict").css("display", "none");
                $("div.errorPredict").css("display", "block");
            });
    });
});

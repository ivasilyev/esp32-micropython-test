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
    alert(JSON.stringify(out))
}

function validateColor(x) {
    console.log(x);
    return x;
}

function validate_animation(x) {
    console.log(x);
    return x;
}

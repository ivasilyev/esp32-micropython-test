const ANIMATIONS = ['random_blink', 'cycle2', 'bounce2'];

function send_post_query(json) {
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

function send_get_query(json) {
    let xhr = new XMLHttpRequest();
    let url = "url?data=" + encodeURIComponent(JSON.stringify(json));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let state = JSON.parse(xhr.responseText);
            console.log('send_get_query', state);
            app.setState(state)
        }
    };
    xhr.send();
}

function request_current_state() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/state', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let state = JSON.parse(xhr.responseText);
            console.log('request_current_state', state);
            app.setState(state)
        }
    };
    xhr.send();
}

function draw_error(element_id, error_description) {
    document.getElementById(element_id).innerHTML = error_description;
}

function validateColor(hex) {
    return (hex.startsWith('#') && hex.length === 7);
}

function validate_animation(animation_name, element_id) {
    if (!ANIMATIONS.includes(animation_name)) {
        alert('Please choose an animation!');
        //draw_error(element_id, 'Please choose an animation!');
        return false;
    }
    return true;
}

class App {
    DEFAULT_STATE = {animation: "", color_transitions: 10, always_lit: false,
                      colors: {color_0: "#f5647f", color_1: "#7cc4e4"}};
    DEFAULT_COLOR = '#000000';

    constructor() {
        this.state = {};
        this.animation_data = JSON.parse(localStorage.getItem('animation_data'));
        request_current_state();
        if (Object.keys(this.state).length === 0) {
            this.setState(this.DEFAULT_STATE);
        }
    }

    render() {
        let a = this.state.animation;
        if (a.length > 0) {
            document.getElementById('animation_dropdown').value = a;
        }
        Object.keys(this.state.colors).forEach((id) => {
            const number = this.parseColorNumber(id);
            const color = this.state.colors[id];
            if (document.getElementById(`color_picker_${number}`) === null ) {
                this.makeColorPicker(number, color);
            }
            else {document.getElementById(`color_${number}`).value = color}
        });
    }

    setState(state) {
        if (Object.keys(state).length > 0) {
            this.state = state;
            this.render();
        }
    }
    
    makeColorPicker(number, color = this.DEFAULT_COLOR) {
        const div = document.getElementById('color_selector');
        div.insertAdjacentHTML('beforeend',
            `<span id="color_picker_${number}"><label for="color_${number}">Color ${number + 1}</label><input type="color" id="color_${number}" name="${number}" value=${color}></span>`);
        this.state.colors[`color_${number}`] = color;
    }
    
    removeColorPicker(number) {
        const span = document.getElementById(`color_picker_${number}`);
        span.remove();
        delete this.state.colors[`color_${number}`];
    }

    parseColorNumber(s) {
        return parseInt(s.match('_([0-9]+)$')[1])
    }

    getLatestColorNumber() {
        return Object.keys(this.state.colors).map(this.parseColorNumber).sort().slice(-1)[0];
    }

    pushColorPicker(color = this.DEFAULT_COLOR) {
        this.makeColorPicker(this.getLatestColorNumber() + 1, color);
    }

    popColorPicker() {
        const latest = this.getLatestColorNumber();
        if (latest > 1) {
            this.removeColorPicker(this.getLatestColorNumber());
        }
        else  {
            alert('Two colors minimum!')
        }
    }

    validateTransitionNumber() {
        const transitionsNumber = parseInt(transitionSlider.value);
        if (transitionsNumber >= 2 || transitionsNumber <= 20) {
            this.state.color_transitions = transitionsNumber;
            return true;
        }
        return false;
    }

    validateFormOnSubmit() {
        let validations = [];
        let animation = document.getElementById('animation_dropdown').value;
        validations.push(validate_animation(animation, 'animation_dropdown'));

        let colors = {};

        Object.keys(this.state.colors).forEach((id) => {
            let color = document.getElementById(id);
            if (color !== null) {
                color = color.value;
                validations.push(validateColor(color));
                colors[id] = color;
            }
        });

        validations.push(this.validateTransitionNumber());

        if (validations.every((x) => {
            return x
        })) {
            let out = {
                colors: colors,
                animation: animation,
                color_transitions: this.state.color_transitions,
                always_lit: this.state.always_lit,
            };
            console.log(out);
            localStorage.setItem('animation_data', JSON.stringify(out));
            send_get_query(out);
        }
    }
}

const app = new App();
const form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
    });
}
document.getElementById('button__submit').addEventListener(
    'click', function(e) {
        app.validateFormOnSubmit();
    });
document.getElementById('button__push_color').addEventListener(
    'click', function(e) {
        app.pushColorPicker();
    });
document.getElementById('button__pop_color').addEventListener(
    'click', function(e) {
        app.popColorPicker();
    });

const transitionSlider = document.getElementById('range__shades');
const transitionInput = document.getElementById('input__shades');
transitionInput.value = transitionSlider.value;

transitionSlider.oninput = () => transitionInput.value = transitionSlider.value;
transitionInput.oninput = () => transitionSlider.value = transitionInput.value;

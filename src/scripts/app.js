import "./fontawesome"
import "./components"
import 'htmx.org';
import Alpine from 'alpinejs';
import Tagify from '@yaireo/tagify';

document.addEventListener('DOMContentLoaded', function () {
    var input = document.querySelector('#tags');
    if (input) {
        console.log("Input element found", input);
        new Tagify(input, {
            whitelist: ["JavaScript", "Python", "Ruby"],
            maxTags: 10,
            dropdown: {
                maxItems: 20,
                classname: "tags-look",
                enabled: 0,
                closeOnSelect: false
            }
        });
    }
});

Alpine.start();

import "./fontawesome";
import Alpine from 'alpinejs';
import Tagify from '@yaireo/tagify';
import '@yaireo/tagify/dist/tagify.css';

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed");
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
    } else {
        console.log("Input element not found");
    }
});

Alpine.start();
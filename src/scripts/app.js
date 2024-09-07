import "./fontawesome";
import "./components"
import "htmx.org";
import Alpine from 'alpinejs';
import Tagify from '@yaireo/tagify';
import Swal from "sweetalert2";

document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('#tags');
    const savedTagsElement = document.querySelector('#saved-tags');

    if (input) {
        const tagify = new Tagify(input, {
            whitelist: ["JavaScript", "Python", "Ruby"],
            maxTags: 1,
            enforceWhitelist: true,
            dropdown: {
                maxItems: 3,
                classname: "tags-look",
                enabled: 0,
                closeOnSelect: false
            }
        });

        if (savedTagsElement?.value) {
            tagify.addTags(JSON.parse(savedTagsElement.value));
        }

        document.querySelector('#search-form').addEventListener('submit', (event) => {
            const selectedTag = tagify.value[0]?.value || " ";
            input.value = selectedTag.trim();
        });
    }
});

window.Swal = Swal;
Alpine.start();

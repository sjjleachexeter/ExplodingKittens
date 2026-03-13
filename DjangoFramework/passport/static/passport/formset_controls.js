
    function setupFormset(formsetId, prefix, initialCount) {
        let formIdx = initialCount;
        let totalForms = $(`#id_${prefix}-TOTAL_FORMS`);

        // Add form
        $(`.add-form-btn[data-target="${formsetId}"]`).click(function () {
            let newForm = $(`${formsetId} .form-row:last`).clone(true);
            newForm.find(":input").each(function () {
                let name = $(this).attr("name");
                if (name) {
                    let newName = name.replace(/-\d+-/, "-" + formIdx + "-");
                    $(this).attr({
                        "name": newName,
                        "id": "id_" + newName,
                    }).val("");
                }
            });
            newForm.show();
            $(formsetId).append(newForm);
            formIdx++;
            totalForms.val(formIdx);
        });

        // Remove form
        $(formsetId).on("click", ".remove-form", function () {
            let visibleForms = $(`${formsetId} .form-row:visible`);
            let row = $(this).closest(".form-row");

            if (visibleForms.length === 1) {
                row.find("input, select, textarea").each(function () {
                    if ($(this).attr("type") === "checkbox") {
                        $(this).prop("checked", false);
                    } else {
                        $(this).val("");
                    }
                });
                return;
            }

            let deleteInput = row.find("input[name$='-DELETE']");
            if (deleteInput.length) {
                deleteInput.prop("checked", true);
                row.hide();
            } else {
                row.remove();
            }
        });
    }

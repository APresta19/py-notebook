 document.addEventListener('DOMContentLoaded', function() {{
                const textarea = document.getElementById('codebox');
                textarea.addEventListener('paste', function(e) {{
                    e.preventDefault();
                    alert("Pasting is disabled!");
             }});
            }});
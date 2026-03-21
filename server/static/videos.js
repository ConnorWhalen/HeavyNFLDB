
function ytClick(url) {
    let yt_embed = document.getElementById("yt-embed");

    yt_embed.removeAttribute("srcdoc");
    yt_embed.setAttribute("src", url);
}

function loadTable(subpage) {
    $('#myTable').DataTable({
        serverSide: true,
        scrollX: true,
        ajax: {
            url: '/video/api/videos',
            dataSrc: 'data',
        },
        columns: [
            { data: 'id' },
            { data: 'type' },
            { data: 'title' },
            { data: 'description' },
            { data: 'upload_date' },
            { data: 'duration_secs' },
            { data: 'thumbnail_url' },
            { data: 'url'},
            { data: 'url'}
        ],
        columnDefs: [
            {
                "targets": 3,
                "data": "description",
                "render": function ( data, type, row, meta ) {
                    return data.replaceAll("\n", "<br/>");
                }
            },
            {
                "targets": 8,
                "data": "video_url",
                "render": function ( data, type, row, meta ) {
                    return '<div onclick="ytClick(\'' + data + '\')" class="yt-link"><u>[YouTube]</u></div>';
                }
            }
        ],
        order: [[4, 'desc']],
        initComplete: function () {
            this.api()
                .columns()
                .every(function () {
                    let column = this;
                    let title = column.footer().textContent;
        
                    // Create input element
                    let input = document.createElement('input');
                    input.classList.add('column-input');
                    input.placeholder = title;
                    column.footer().replaceChildren(input);
        
                    // Event listener for user input
                    input.addEventListener('keyup', () => {
                        if (column.search() !== this.value) {
                            column.search(input.value).draw();
                        }
                    });
                });
        }
    });
}

$(document).ready(function () {
    loadTable();
});

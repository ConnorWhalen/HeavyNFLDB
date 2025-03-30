function ytClick(element) {
    document.getElementById("yt-embed").setAttribute("src", element.innerText);
}

$(document).ready( function () {
    $('#myTable').DataTable({
        serverSide: true,
        scrollX: true,
        ajax: {
            url: '/api/songs',
            dataSrc: 'data',
        },
        columns: [
            { data: 'title' },
            { data: 'artist' },
            { data: 'album' },
            { data: 'hometown' },
            { data: 'release_date' },
            { data: 'genre' },
            { data: 'label' },
            { data: 'video_url'}
        ],
        columnDefs: [
            {
                "targets": 1,
                "data": "artist",
                "render": function ( data, type, row, meta ) {
                    return '<a href="/artist/'+row['artist_id']+'" target="_blank">'+data+'</a>';
                }
            },
            {
                "targets": 2,
                "data": "album",
                "render": function ( data, type, row, meta ) {
                    return '<a href="/album/'+row['album_id']+'" target="_blank">'+data+'</a>';
                }
            },
            {
                "targets": 7,
                "data": "video_url",
                "render": function ( data, type, row, meta ) {
                    // return '<a href="'+data+'" target="_blank">'+data+'</a>';
                    return '<div onclick="ytClick(this)">'+data+'</a>';
                }
            }
        ],
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
} );
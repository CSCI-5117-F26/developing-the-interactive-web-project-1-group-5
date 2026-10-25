WITH new_image AS (
    INSERT INTO images (filename, mimetype, data)
    VALUES (
        'my-image.png',
        'image/png',
        pg_read_binary_file('/absolute/path/to/my-image.png')
    )
    RETURNING imageId
)
INSERT INTO nodes (
    title,
    description,
    imgId,
    category
)
SELECT
    'My Node',
    'Description of my node',
    imageId,
    TRUE
FROM new_image
RETURNING *;
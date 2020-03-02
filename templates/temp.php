<?php
            if(isset($_POST["btnSubmit"]))
            {
            echo $_Files['file'],
            }
?>

<html>
    <head>
        <title>PHP upload file demo</title>
    </head>
    <body>
        <form method="post" enctype="multipart/form-data" name="formUploadFile">
            <label>Select single file to upload lodo:</label>
            <input type="file" name="file"/>
            <input type="submit" value="Upload File" name="btnSubmit"/>
        </form>
    </body>
</html>
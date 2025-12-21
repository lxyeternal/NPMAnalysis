# Four ways of echoing JHS lists into an HTML document

```javascript
<?jhs
    const star_trek = [
        'William Shatner as Admiral James T. Kirk',
        'Leonard Nimoy as Spock',
        'Nichelle Nichols as Nyota Uhura',
        'DeForest Kelley as Leonard McCoy',
        'Gene Roddenberry as the Creator',
        'George Takei as Hikaru Sulu',
        'James Doohan  as Scotty',
        'Walter Koenig as Pavel Chekov'
    ];
?>
<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
</head>
<body>
<?jhs 
    echo('<ul>');
        for(var i=0;i<star_trek.length;i++){
        echo('<li>'+star_trek[i]+'</li>');
        }
    echo('</ul>');
?>

<br>
<?jhs 
    echo('<ul>');
        star_trek.forEach(item=>{
        echo('<li>'+item+'</li>');
        });
    echo('</ul>');
?>

<br>

<ul>
<?jhs for(var i=0;i<star_trek.length;i++){ ?>
 <li><?jhs echo(star_trek[i]) ?></li>
 <?jhs } ?>
</ul>

<br>

<ul>
<?jhs star_trek.forEach(item=>{ ?>
 <li><?jhs echo(item) ?></li>
 <?jhs }); ?>
</ul>
</body>
</html>
```

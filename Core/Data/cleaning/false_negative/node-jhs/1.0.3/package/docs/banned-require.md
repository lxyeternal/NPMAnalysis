# Banned Require

## You can prevent some NODEjs modules to be loaded in your JHS scripts

There are two nodejs modules that you are not allowed to require (include) in  a JHS script: These are: require ('vm') and require ('jhs'). In addition, you can ban other modules, too, by adding an array of names of modules to be banned in the options JSON, when you are creating a JHS instance in your server script.

 ```javascript
    const options = {banned_require:['xx-node','lib-y','alt-z']};
    const execjhs = new JHS(options);
 ```

  in this example node modules  (even installed globally or locally in your project) the modules called 'xx-node','lib-y','alt-z' (along with 'vm' and 'jhs') are banned in the server. That means, you require any of them, a server error will be thrown.

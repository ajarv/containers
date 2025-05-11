
```bash
# install docker

https://docs.docker.com/engine/install/ubuntu/




```



```bash

export SHOST=s3.dev.anomili.com 
echo -n | openssl s_client -connect 192.168.1.47:443 -servername ${SHOST} | openssl x509 -noout -text | grep ${SHOST} 

export SHOST=minio.dev.anomili.com 
echo -n | openssl s_client -connect 192.168.1.47:443 -servername ${SHOST} | openssl x509 -noout -text | grep ${SHOST} 

curl -k https://192.168.1.47

https://minio.dev.anomili.com/

```
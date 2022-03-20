### Observe what files are stored
```
strings disk* > allStrings.txt
cat allStrings.txt |grep -e txt -e pdf -e jpg
```

### The first guess
```
sudo mdadm --examine disk01.img
```

### Volume isn't encrypted 
#### a lot of images and txt files. 

# Search for a text as a strating point. 

```
for f in *.img; do
rec="$(strings $f |grep "I will appeach the vill" )"
if [[ -n "$rec" ]] ; then echo $f;  fi;
done
```

Treason, foul treason! Villain! traitor! slave!

5

```
strings disk05.img | grep -i -b 550 -A 550 "appeach"
```


### Repeat the process to cover all disks
### order of blocks
5,2,8,9,10,1,7,4,6,3
### Bit shift cycle since that is the order
### Don't use 10 drives. Just loopback them. 
```
sudo losetup /dev/loop1 disk01.img
sudo losetup /dev/loop2 disk02.img
sudo losetup /dev/loop3 disk03.img
sudo losetup /dev/loop4 disk04.img
sudo losetup /dev/loop5 disk05.img
sudo losetup /dev/loop6 disk06.img
sudo losetup /dev/loop7 disk07.img
sudo losetup /dev/loop8 disk08.img
sudo losetup /dev/loop9 disk09.img
```

### Eventually the assembly will succeed
#### The main expectation that is RAID5 isn't FAILED.(It is still valid raid5 with maximum 1 failed drive)
```
sudo mdadm  --create  --assume-clean --force --verbose  --level=5 --chunk=4 --raid-devices=10  /dev/md0 /dev/loop1 /dev/loop7 /dev/loop4 /dev/loop6 /dev/loop3 /dev/loop5 /dev/loop2 /dev/loop8 /dev/loop9 /dev/loop10
 
sudo mount /dev/md0 mnt/ 
 
sudo chmod 777  /mnt/*
sudo losetup /dev/loop10 disk10.img
```

#### Look over files and get the flag.

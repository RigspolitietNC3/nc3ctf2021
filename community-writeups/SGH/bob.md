# bob

Vi er blevet givet en fil indeholdende noget der ligner en sangtekst.

    00000000: 0d00 0000 1700 6800 01f3 01e4 01d1 01c5  ......h.........
    00000010: 01b1 0199 018b 0172 015b 014a 012e 0117  .......r.[.J....
    00000020: 0106 00f7 00e7 00db 00cc 00bb 00ab 009a  ................
    00000030: 008d 0075 0068 0000 0000 0000 0000 0000  ...u.h..........
    00000040: 0000 0000 0000 0000 0000 0000 0000 0000  ................
    00000050: 0000 0000 0000 0000 0000 0000 0000 0000  ................
    00000060: 0000 0000 0000 0000 0886 8ef0 7603 0017  ............v...
    00000070: 4920 7369 7413 868e ca72 0300 2d68 6561  I sit....r..-hea
    00000080: 6469 6e67 2073 7472 6169 6768 7408 8599  ding straight...
    00000090: d66b 0300 1767 686f 7374 0c85 95c8 6503  .k...ghost....e.
    000000a0: 001f 6974 2773 206a 7573 740b 83ed e072  ..it's just....r
    000000b0: 0300 1d61 6e64 2068 6572 650c 83cd e86e  ...and here....n
    000000c0: 0300 1f74 656c 6570 686f 6e65 0a83 c8c2  ...telephone....
    000000d0: 2003 001b 616e 6420 796f 7507 83bb 8726   ...and you....&
    000000e0: 0300 156d 6f6f 6e0b 83b8 c06b 0300 1d74  ...moon....k...t
    000000f0: 6861 7420 7468 650a 83ad d665 0300 1b69  hat the....e...i
    00000100: 7320 6675 6c6c 0c83 a5c2 6d03 001f 4927  s full....m...I'
    00000110: 6420 6b6e 6f77 6e12 839d dd43 0300 2b68  d known....C..+h
    00000120: 6572 6520 636f 6d65 7320 796f 7572 1783  ere comes your..
    00000130: 95e4 2c03 0035 6167 6169 6e20 6275 7420  ..,..5again but 
    00000140: 7468 6174 2773 206e 6f74 0c83 95e4 2003  that's not.... .
    00000150: 001f 7965 6172 7320 6167 6f12 8394 c064  ..years ago....d
    00000160: 0300 2b68 6561 7269 6e67 2061 2076 6f69  ..+hearing a voi
    00000170: 6365 1483 85dc 7403 002f 6120 636f 7570  ce....t../a coup
    00000180: 6c65 206f 6620 6c69 6768 7409 8385 dc20  le of light.... 
    00000190: 0300 1964 616d 6e65 6413 82b9 8633 0300  ...damned....3..
    000001a0: 2d68 6170 7065 6e65 6420 746f 2063 616c  -happened to cal
    000001b0: 6c0f 8291 f26c 0300 2577 656c 6c20 4927  l....l..%well I'
    000001c0: 6c6c 2062 6507 81dc ea7d 0300 1566 616c  ll be....}...fal
    000001d0: 6c0e 8181 e475 0300 2368 616e 6420 6f6e  l....u..#hand on
    000001e0: 2074 6865 0a81 81cf 4303 001b 756e 7573   the....C...unus
    000001f0: 7561 6c08 8180 e239 0300 1766 6f72 2061  ual....9...for a

Lidt googling og det viser sig at være "Diamonds and Rust"
af Joan Baez. <https://genius.com/Joan-baez-diamonds-and-rust-lyrics>

Teksten er i forkert rækkefølge og det ligner at der er 8 bytes gibberish foran hver del af teksten. Vi kan sætte dem i korrekt rækkefølge og vi får følgende.

      0F 82 91 F2 6C 03 00 25 well I'll be
      09 83 85 DC 20 03 00 19 damned
      12 83 9D DD 43 03 00 2B here comes your
      08 85 99 D6 6B 03 00 17 ghost
      17 83 95 E4 2C 03 00 35 again but that's not
      0A 81 81 CF 43 03 00 1B unusual
      0C 85 95 C8 65 03 00 1F it's just
      0B 83 B8 C0 6B 03 00 1D that the
      07 83 BB 87 26 03 00 15 moon
      0A 83 AD D6 65 03 00 1B is full
      0A 83 C8 C2 20 03 00 1B and you
      13 82 B9 86 33 03 00 2D happened to call
      0B 83 ED E0 72 03 00 1D and here
      08 86 8E F0 76 03 00 17 I sit
      0E 81 81 E4 75 03 00 23 hand on the
      0C 83 CD E8 6E 03 00 1F telephone
      12 83 94 C0 64 03 00 2B hearing a voice
      0C 83 A5 C2 6D 03 00 1F I'd known
      14 83 85 DC 74 03 00 2F a couple of light
      0C 83 95 E4 20 03 00 1F years ago
      13 86 8E CA 72 03 00 2D heading straight
      08 81 80 E2 39 03 00 17 for a
      07 81 DC EA 7D 03 00 15 fall

Herfra brugte vi mange timer på at finde ud af hvad de 8 bytes var. Derudover så er der også noget fnidder i starten af filen. Det kunne ligne noget 3DES (opgaven nævner jo også 3 x bob).

NC3 frigav et hint hvor de nævner noget med "lite databaser" og "hvilken page-type starter med 0x0D?". Ok - så ved vi at det er en type 0xD sqlite3 page (A value of 13 (0x0d) means the page is a leaf table b-tree page.)

<https://www.sqlite.org/fileformat.html>

Ved at læse dokumentationen og gå filen igennem finder vi ud af at tekstlinie (inkl. de 8 foranstillede bytes) må være "Table B-Tree Leaf Cell (header 0x0d)".

Hver cellheader starter med en varint som angiver den totale længde af den aktuelle cell. En sqlite3 varint er en multibyte int64. Man anvender kun de nederste 7 bit i hver byte. Bit7 angiver om der er flere bytes. Den officielle dokumentation er lidt inviklet synes jeg.

> A variable-length integer or "varint" is a static Huffman encoding of 64-bit twos-complement integers that uses less space for small positive values. A varint is between 1 and 9 bytes in length. The varint consists of either zero or more bytes which have the high-order bit set followed by a single byte with the high-order bit clear, or nine bytes, whichever is shorter. The lower seven bits of each of the first eight bytes and all 8 bits of the ninth byte are used to reconstruct the 64-bit twos-complement integer. Varints are big-endian: bits taken from the earlier byte of the varint are more significant than bits taken from the later bytes.

Man kan decode en varint med følgende C-funktion

```C
static int64_t read_varint(uint8_t** ptr) {
    int64_t res = 0;
	uint8_t ch;
    do {
		ch = **ptr;
		res <<= 7;
		res |= ch & 0x7f;
		(*ptr)++;
	} while (ch & 0x80);
	return res;
}
```

Længderne på hver cell er følgende:
    
    0x44796C 
    0x616E20 
    0x676EC3 
    0xA66B6B 
    0x65722C 
    0x2067C3 
    0xA56465 
    0x6E206B 
    0x6EC3A6 
    0x6B6B65 
    0x722120 
    0x4E4333 
    0x7B7072 
    0xC3B876 
    0x207275 
    0x73746E 
    0x652064 
    0x69616D 
    0x616E74 
    0x657220 
    0xC3A572 
    0x203139 
    0x37357D 


Det er nogle giftige længder - og de passer slet ikke med den faktiske payload. Gad vide hvilket tegn de enkelte bytes i de længder er.

    44796C      44 D     79 y     6C l 
    616E20      61 a     6E n     20   
    676EC3      67 g     6E n     C3 � 
    A66B6B      A6 �     6B k     6B k 
    65722C      65 e     72 r     2C , 
    2067C3      20       67 g     C3 � 
    A56465      A5 �     64 d     65 e 
    6E206B      6E n     20       6B k 
    6EC3A6      6E n     C3 �     A6 � 
    6B6B65      6B k     6B k     65 e 
    722120      72 r     21 !     20   
    4E4333      4E N     43 C     33 3 
    7B7072      7B {     70 p     72 r 
    C3B876      C3 �     B8 �     76 v 
    207275      20       72 r     75 u 
    73746E      73 s     74 t     6E n 
    652064      65 e     20       64 d 
    69616D      69 i     61 a     6D m 
    616E74      61 a     6E n     74 t 
    657220      65 e     72 r     20   
    C3A572      C3 �     A5 �     72 r 
    203139      20       31 1     39 9 
    37357D      37 7     35 5     7D } 
    
Hovsa - hvis vi nøjes med tegnene får vi flaget.

    Dylan gnækker, gåden knækker! NC3{prøv rustne diamanter år 1975}
    
```C
#include <stdio.h>
#include <inttypes.h>

static int64_t read_varint(uint8_t** ptr) {
    int64_t res = 0;
	uint8_t ch;
    do {
		ch = **ptr;
		res <<= 7;
		res |= ch & 0x7f;
		(*ptr)++;
	} while (ch & 0x80);
	return res;
}

static int offsets[23] {
	0x1b9, 0x193, 0x11f, 0x95 , 0x136, 0x1ec, 0xa2 , 0xef,
	0xe3 , 0xff , 0xd4 , 0x1a1, 0xb3 , 0x70 , 0x1d9, 0xc3,
	0x163, 0x10e, 0x17a, 0x152, 0x7d , 0x1fb, 0x1cd };

int main() {
	uint8_t buf[1024];
	auto fp = fopen("bob", "rb");
	auto len = fread(buf, 1, sizeof(buf), fp);
	fclose(fp);

	for (auto i=0; i<23; i++) {
		uint8_t *header_start = &buf[offsets[i] - 8];
		uint8_t *ptr = header_start;

		auto v = (uint64_t)read_varint(&ptr);
		printf("%c",   (v >>16) & 0xff);
		printf("%c",   (v >>8)  & 0xff);
		printf("%c",   (v >>0)  & 0xff);
	}
	printf("\n");
}
```

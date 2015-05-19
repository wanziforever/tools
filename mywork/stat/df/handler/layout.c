#define MAX_BOX 20
char layout[MAX_BOX];
memset(layout, 0, MAX_BOX);

// from a position to find the next free box
int findNextValid(int start) {
  int found = 0;
  for (int i=start; start < MAX_BOX; i++) {
    if (layout[i] == 1 )
       continue;
    found = 1;
    break;
  }
  if (found)
       return i;
  return -1;
}

// from a position, to fillin the region which a x axis, and a y axis hold
int occupy(int start, int x, int y) {
  char a = layout[start];
  for (int i=0; i<x, i++) {
    for (int j=0; j<y, j++)
       a[i][j] = 1;
  }
}

int generatePoster(int pos) {
  // generate the poster base on the position index
  return 1
}

elem_ite = parseXML(xml_input);
for (elem = elem_ite.begin(); elem != elem_ite.end(); elem = elem_ite.next()) {
  int pos = findNextValid(elem.id-1);
  // exchange the x, y axis data as the input of occupy menthod
  occupy(pos, elem.ylen, elem.xlen);
  generatePoster(pos);
}


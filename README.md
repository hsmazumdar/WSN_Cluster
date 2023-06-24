# WSN_Cluster
A Simple Clustering Algorithm for Wireless Sensor Networks (WSN)

Algorithm:

1. Start
2. nodsz = Get number of nodes
3. grpssz = Get number of clusters
4. grpsz[] = Get node size of each clusters (temp only)
5. dist[][] = Get distance between all nodes
i = 0;
best = a big number;
loop1:
	chn = Get furthest node as cluster head node ch_i
	Mark grpsz[i] nearest cluster members state as -1
	Choos new cluster head in center of gravity of i_th cluster as ch_i
	i = i + 1
	if (i < grpssz) 
	 Goto loop1
goodness = sum of distance between all cluster-heads to members
Include nearest members of other groups to each ch by excluding from present group
if(best > goodness)
	Goto loop1  
Update grpsz[]
Result: Mark all cluster heads with cluster members	 
End

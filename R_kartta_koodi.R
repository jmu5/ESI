library(ggplot2)
library(grid)
library(rworldmap)
install.packages("rworldmap")
library(rworldmap)                 
install.packages("mapproj")
library(mapproj)

args<-commandArgs(TRUE)
sector<-args[1]


value<-read.delim("heatmap.csv", header=F, sep=";")
value<-as.numeric(value)

worldMap<-getMap()
getMap()[['NAME']]
europeanUnion<-c("Albania","Austria","Belgium","Bulgaria","Cyprus","CzechRep.",
                 "Germany","Denmark","Estonia","Greece","Spain","Finland","France",
                 "Croatia","Hungary","Ireland","Italy","Lithuania","Luxembourg","Latvia",
                 "Montenegro","North Macedonia","Malta","Netherlands","Poland","Portugal",
                 "Romania","Serbia","Sweden","Slovenia","Slovakia","Turkey")

indEU<-which(worldMap$NAME%in%europeanUnion)

europeCoords<-lapply(indEU, function(i){
  df<-data.frame(worldMap@polygons[[i]]@Polygons[[1]]@coords)
  df$region = as.character(worldMap$NAME[i])
  colnames(df) <- list("long", "lat", "region")
  return(df)
})
europeCoords <- do.call("rbind", europeCoords)
table<-data.frame(country=europeanUnion, value=value)
europeCoords$value<-table$value[match(europeCoords$region, table$country)]
P<-ggplot()+geom_polygon(data=europeCoords, aes(x=long,y=lat,group=region,fill=value), colour="black",size=0.1)+coord_map(xlim=c(-13,35),ylim=c(32,71))
P<-P+scale_fill_gradient(name=paste("Subsector ", sector, " confidence"), low="#FF0000FF", high="#FFFF00FF", na.value="grey50")
P<-P+theme(#panel.grid.minor=element_line(colour=NA), panel.grid.minor=element_line(colour=NA), #panel.background=element_rect(fill=NA, colour=NA),axis.text.x=element_blank(), axis.text.y=element_blank(), axis.ticks.x=element_blank(),axis.ticks.y=element_blank(), axis.title=element_blank(), #rect=element_blank(), plot.margin=unit(0*c(-1.5,-1.5,-1.5,-1.5), "lines"))
)

jpeg("heatmap.jpg")
P
dev.off()

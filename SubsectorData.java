import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.Clock;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.lang.Double;
import java.lang.Integer;
import java.util.Arrays;
import java.text.ParseException;
import java.text.NumberFormat;
import java.io.File;
import java.io.FileInputStream;
import java.util.Iterator;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.sqlite.*;

public class SubsectorData{

    public static void main(String[] args){

        Connection conn=null;

        try{
            Class.forName("org.sqlite.JDBC");
            String url="jdbc:sqlite:/var/www/html/ESI/ESI.db.sqlite";
            conn=DriverManager.getConnection(url);
            System.out.println("Connection to SQLite has been established.");
        }catch(Exception e){
            System.out.println(e.getMessage());
        }finally{
            try{
                if(conn!=null){
                    conn.close();
                }
            }catch(SQLException ex){
                System.out.println(ex.getMessage());
            }
        }

        long start=System.currentTimeMillis();

        try{
            File file = new File("/var/www/html/java/industry_subsectors_sa_m_nace2.xlsx");
            FileInputStream fis = new FileInputStream(file);

            //BufferedReader br = new BufferedReader(new InputStreamReader(fis));

            XSSFWorkbook wb = new XSSFWorkbook(fis);
            XSSFSheet sheet = wb.getSheetAt(0);

            System.out.println("Sheets: " + wb.getNumberOfSheets());
//            int country=0;
            String[] countries=new String[] {"EU","EA","BE","BG","CZ","DK","DE","EE","IE","EL","ES","FR","HR","IT","CY","LV","LT","LU","HU","MT","NL","AT","PL","PT","RO","SI","SK","FI","SE","UK","ME","MK","AL","RS","TR"};
            int[] subsectors={10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33};

            for(int i=0; i<0/*wb.getNumberOfSheets()-2*/; i++){ 

              sheet=wb.getSheetAt(i+2);
              Iterator<Row> itr = sheet.iterator();
              int year=1985;
              int monthindex=0;
              String month="";

              while(itr.hasNext()){
              
                  Row row = itr.next();
                   
                  int multiple=0;
                  int q=0;
                  int cellcount=0;
                  int country=0;

                  if(monthindex>12){
                      monthindex=1;
                      year++;
                  }
                  if(monthindex<10){
                      month="0"+Integer.toString(monthindex);
                  }else{
                      month=Integer.toString(monthindex);
                  }
                  String date=year+"-"+month+"-01";
                  String query="";
                  String values="";
                  String sql="";
                  boolean hasValues=false;

                  System.out.println("Subsector:"+subsectors[i]+" Row num:"+row.getRowNum()+" Cells:"+row.getLastCellNum());

                  for (int cellindex=1; cellindex<row.getLastCellNum(); cellindex++) {
 
                      if(row.getRowNum()!=0){
                          //System.out.print("Country:"+countries[country]+" ");
                          if(cellindex%8==1){
                              query="INSERT INTO INDUSTRIAL (date, country, subsector";
                              values=" )VALUES("+date+", " + countries[country].toString()+ ", "+  Integer.toString(subsectors[i]);
                              sql="";
                              hasValues=false;
                          }
                          Cell cell = row.getCell(cellindex);
//                          System.out.print(date+", "+countries[country]+", "+ subsectors[i]+" row num:" +row.getRowNum()+" cellindex:"+cellindex);

                          switch(cell.getCellType()){
                              case Cell.CELL_TYPE_STRING:
  //                              System.out.print(cell.getStringCellValue() + " - ");
                                  break;
                              case Cell.CELL_TYPE_NUMERIC:
                                  if(cellindex%8==1){
                                      query=query+", cof";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==2){
                                      query=query+", q1";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==3){
                                      query=query+", q2";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==4){
                                      query=query+", q3";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==5){
                                      query=query+", q4";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==6){
                                      query=query+", q5";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==7){
                                      query=query+", q6";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      break;
                                  }
                                  if(cellindex%8==0){//if(q==7){
                                      query=query+", q7";
                                      values=values+", "+cell.getNumericCellValue();
                                      hasValues=true;
                                      //sql=query+values+")";
                                      break;
                                  }
                              default:
                          }
                          sql=query+values+")";
                          if(cellindex%8==0){
                              country++;
                              if(hasValues){System.out.println(sql);}
                              hasValues=false;
                          }
                      }

}
//                System.out.println(sql);
                monthindex++;
//                cal.add(Calendar.MONTH, 1);}
}	
}
}
        catch(Exception e){
            e.printStackTrace();
        }
        long end=System.currentTimeMillis();
        System.out.println("Time: "+(end-start)/1000+"s");
    }
}

// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class GetTicketNumber extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject get_info(String host, String contract_address, String prop) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/VoteEX/GetTicketNumber.py",host,contract_address,prop);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
                while ((line = reader.readLine()) != null) {
			try{
        		        result.put("output",line);
	                }catch(Exception e){ line = e.getMessage();}
                }
		//try{
		//	result.put("host",host);
			//result.put("contract_address",contract_address);
			//result.put("prop",prop);
		//}catch(Exception e){}
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	String host = request.getParameter("host");
	String contract_address = request.getParameter("contract_address");
	//String prop = request.getParameter("prop");
	String prop = new String(request.getParameter("prop").getBytes("iso-8859-1"), "UTF-8");
	

	JSONObject result = new JSONObject();
	result = get_info(host,contract_address,prop);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}

	response.setContentType("text/html;charset=UTF-8");

   }

   public void destroy() {
      // do nothing.
   }
}

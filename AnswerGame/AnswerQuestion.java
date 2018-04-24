// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class AnswerQuestion extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject contract_deploy(String host,String account,String passwd, String contract_address, String answer) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/AnswerGame/w.py",host,account,passwd,contract_address,answer);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
		try{
			result.put("host",host);
			result.put("account",account);
			result.put("passwd",passwd);
			result.put("contract_address",contract_address);
			result.put("answer",answer);
		}catch(Exception e){}
		/*
                while ((line = reader.readLine()) != null) {
			try{
				if(line.contains("wait"))continue;
				else if(line.contains("account : ")){
					result.put("account",line.split("account : ")[1]);
				}
				else if(line.contains("contract address : ")){
					result.put("contract address",line.split("contract address : ")[1]);
				}
				else if(line.contains("contract abi : ")){
					result.put("abi",line.split("contract abi : ")[1]);
				}
			}catch(Exception e){}
                        }
		*/
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	//JSONObject joParam = request.getParameter(request);
	//String host = joParam.optString("host");
	//String account = joParam.optString("account");
	//String passwd = joParam.optString("passwd");
	String host = request.getParameter("host");
	String account = request.getParameter("account");
	String passwd = request.getParameter("passwd");
	//String answer = request.getParameter("answer");
	String contract_address = request.getParameter("contract_address");
	String answer = new String(request.getParameter("answer").getBytes("iso-8859-1"), "UTF-8");
	//String question = request.getParameter("question");
	

	JSONObject result = new JSONObject();
	result = contract_deploy(host,account,passwd,contract_address,answer);
	try{
		result.put("result","0");
		//result.put("answer",answer);
		//result.put("deadline",duration);
		result.write(response.getWriter());
	}catch(Exception e){}
      
      // Set response content type
      ///response.setContentType("text/html");

      // Actual logic goes here.
      ///PrintWriter out = response.getWriter();
      ///out.println("<h1>" + message + "</h1>");
   }

   public void destroy() {
      // do nothing.
   }
}

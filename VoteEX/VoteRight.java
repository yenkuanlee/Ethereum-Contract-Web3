// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class VoteRight extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject contract_deploy(String host,String account,String passwd, String contract_address, String voter) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
		if(voter.equals("AllUser"))
                	pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/VoteEX/GiveRightToVoters.py",host,account,passwd,contract_address);
		else
			pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/VoteEX/GiveRightToVoters.py",host,account,passwd,contract_address,voter);
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
			result.put("voter",voter);
		}catch(Exception e){}
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	String host = request.getParameter("host");
	String account = request.getParameter("account");
	String passwd = request.getParameter("passwd");
	String voter = request.getParameter("voter");
	String contract_address = request.getParameter("contract_address");
	

	JSONObject result = new JSONObject();
	result = contract_deploy(host,account,passwd,contract_address,voter);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}
   }

   public void destroy() {
      // do nothing.
   }
}

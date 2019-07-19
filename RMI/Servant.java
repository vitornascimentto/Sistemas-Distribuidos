package SD;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;

public class Servant extends UnicastRemoteObject implements Service {

    // Construtor da Classe
    public Servant() throws RemoteException {
        super();
        System.out.println("Server Started");
    }

    // Método Echo Sobreescrito que vai receber o CPF
    @Override
    public String echo(String cpf) throws RemoteException {
            
        ArrayList<Integer> cpf1 = new ArrayList();
        ArrayList<Integer> cpf2 = new ArrayList();
       
        for (int i = 0; i < cpf.length(); i++) {
            cpf1.add(Integer.parseInt(cpf.substring(i, i + 1)));
        }
        
        for (int i = 0; i < cpf.length() - 2; i++){
            cpf2.add(Integer.parseInt(cpf.substring(i, i + 1)));
        }        
        
        cpf2.add(cpfCalculator(cpf2));
        cpf2.add(cpfCalculator(cpf2));
        
        if (cpf1.equals(cpf2))
            return "CPF Válido";
        else
            return "CPF Não Válido";
        
    }
    
    // Método que vai calcular os dois últimos dígitos do CPF
    public int cpfCalculator(ArrayList<Integer> array){
        
        int soma = 0;
        int mult = 10;
        
        if (array.size() == 10)
            mult = 11;
        
        for (int i = 0; i < array.size(); i++){
            soma += array.get(i) * mult;
            mult -= 1;
        }
         
        int result = soma % 11;
        
        if (result <= 1)
            return 0;
        else
            return 11 - result;        
    
    }

}

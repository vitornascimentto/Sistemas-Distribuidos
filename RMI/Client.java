import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.net.MalformedURLException;
import java.rmi.RemoteException;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws MalformedURLException, RemoteException, NotBoundException {

        // Pedindo o cpf ao Cliente
        System.out.print("Digite um cpf: ");
        Scanner s = new Scanner(System.in);
        String cpf = s.nextLine();

        // Objeto instanciado com o endereço do localhost
        Service service = (Service) Naming.lookup("rmi://localhost:5099/CPF");

        // Requisição da função ao servidor
        System.out.println("Chamando função no servidor: " + service.echo(cpf));

    }
}
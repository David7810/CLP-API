(define (problem more)
(:domain sorting)
    
    (:objects
        atuador_simples1 atuador_simples2 at_null - atuador_simples
        atuador_duplo1 - atuador_duplo
        esteira - esteira
        
        
        peqnmet peqmet mednmet medmet grdnmet grdmet - caracteristica
        
        
        item1 item2 item3 item4 item5 - item
        box1 box2 box3 - location
        inicio - inicio
        box4 - fim
        
        
    )
    
    (:init
    
        (connected atuador_simples1 grdmet)
        (connected atuador_simples1 peqnmet)
        
        (connected atuador_simples2 peqmet)
        (connected atuador_simples2 mednmet)
        
        
        (connected atuador_duplo1 medmet)
        (connected atuador_duplo1 grdnmet)
        ;;(retracted atuador_duplo1)
        
        (type item1 grdmet)
        (type item2 peqmet)
        (type item3 medmet)
        (type item4 peqnmet)
        (type item5 grdnmet)

        
        
        
        (at inicio item1)
        ;;(at inicio item2)
        ;;(at inicio item3)
        ;;(at inicio item4)
        ;;(at inicio item5)
        (link item1 item2)
        (link item2 item3)
        (link item3 item4)
        (link item4 item5)
        
        (at box1 atuador_simples1)
        (at box2 atuador_simples2)
        (at box3 atuador_duplo1)
        (at box4 at_null)
        
    )
    
    (:goal (and
        
        (at box1 item1)
        (at box2 item2)
        (at box3 item3)
        
        (at box1 item4)
        (at box4 item5)
        ;;(at box3 item5)
        
        (not (ligado esteira))
        


    ))
)
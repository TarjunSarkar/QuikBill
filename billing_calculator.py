
import React, { useState, useEffect, useRef } from "react";
import { toast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { SearchIcon, Share2, Trash2, Download } from "lucide-react";
import BillingCalculator from "@/components/BillingCalculator";

interface Calculation {
  id: string;
  productName: string;
  amount: number;
  amountUnit: string;
  amountQty: number;
  gst: number;
  transport: number;
  transportUnit: string;
  transportQty: number;
  total: number;
}

interface SavedBill {
  name: string;
  date: string;
  calculations: Calculation[];
  totalBill: number;
}

const Index = () => {
  const [calculators, setCalculators] = useState<string[]>(['calc-1']);
  const [customerName, setCustomerName] = useState<string>('');
  const [calculationData, setCalculationData] = useState<{ [key: string]: Calculation }>({
    'calc-1': {
      id: 'calc-1',
      productName: '',
      amount: 0,
      amountUnit: 'KG',
      amountQty: 0,
      gst: 0,
      transport: 0,
      transportUnit: 'KG',
      transportQty: 0,
      total: 0
    }
  });
  const [savedBills, setSavedBills] = useState<SavedBill[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [confirmDialogOpen, setConfirmDialogOpen] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<string>('');
  const [historyDialogOpen, setHistoryDialogOpen] = useState<boolean>(false);
  const [selectedBill, setSelectedBill] = useState<SavedBill | null>(null);
  const [userLoggedIn, setUserLoggedIn] = useState<boolean>(false);
  const [historyDeleteDialogOpen, setHistoryDeleteDialogOpen] = useState<boolean>(false);
  const [historyDeleteIndex, setHistoryDeleteIndex] = useState<number>(-1);

  # Load saved bills from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem('billHistory');
    if (savedData) {
      setSavedBills(JSON.parse(savedData));
    }
  }, []);

  # Calculate total bill across all calculators
  const calculateTotalBill = () => {
    return Object.values(calculationData).reduce((sum, calc) => sum + calc.total, 0);
  };

  # Update calculation data for a specific calculator
  const updateCalculationData = (id: string, data: Calculation) => {
    setCalculationData(prev => ({
      ...prev,
      [id]: data
    }));
  };

  # Add a new calculator
  const addCalculator = () => {
    const newId = `calc-${calculators.length + 1}`;
    setCalculators([...calculators, newId]);
    setCalculationData(prev => ({
      ...prev,
      [newId]: {
        id: newId,
        productName: '',
        amount: 0,
        amountUnit: 'KG',
        amountQty: 0,
        gst: 0,
        transport: 0,
        transportUnit: 'KG',
        transportQty: 0,
        total: 0
      }
    }));
    toast({
      title: "Calculator Added",
      description: "A new calculator has been added to your session."
    });
  };

  # Delete a calculator
  const deleteCalculator = (id: string) => {
    setDeleteId(id);
    setConfirmDialogOpen(true);
  };

  # Confirm deletion of a calculator
  const confirmDelete = () => {
    if (calculators.length > 1) {
      const newCalculators = calculators.filter(calcId => calcId !== deleteId);
      setCalculators(newCalculators);
      
      const newCalculationData = { ...calculationData };
      delete newCalculationData[deleteId];
      setCalculationData(newCalculationData);
      
      toast({
        title: "Calculator Deleted",
        description: "The calculator has been removed from your session."
      });
    } else {
      toast({
        title: "Cannot Delete",
        description: "You need to have at least one calculator.",
        variant: "destructive"
      });
    }
    setConfirmDialogOpen(false);
  };

  # Save all calculations as a bill
  const saveBill = () => {
    if (!customerName.trim()) {
      toast({
        title: "Name Required",
        description: "Please enter a customer name to save the bill.",
        variant: "destructive"
      });
      return;
    }

    const calculations = Object.values(calculationData);
    const totalBill = calculateTotalBill();
    
    const newBill: SavedBill = {
      name: customerName,
      date: new Date().toISOString(),
      calculations: calculations,
      totalBill: totalBill
    };

    const updatedBills = [...savedBills, newBill];
    setSavedBills(updatedBills);
    localStorage.setItem('billHistory', JSON.stringify(updatedBills));
    
    toast({
      title: "Bill Saved",
      description: `Bill for ${customerName} has been saved successfully.`
    });
  };

  # Show history
  const viewHistory = () => {
    setHistoryDialogOpen(true);
  };

  # Show bill details
  const viewBillDetails = (bill: SavedBill) => {
    setSelectedBill(bill);
  };

  # Filter bills by search term
  const filteredBills = savedBills.filter(bill => 
    bill.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  # Delete history item
  const confirmHistoryDelete = () => {
    if (historyDeleteIndex >= 0) {
      const updatedBills = [...savedBills];
      updatedBills.splice(historyDeleteIndex, 1);
      setSavedBills(updatedBills);
      localStorage.setItem('billHistory', JSON.stringify(updatedBills));
      
      toast({
        title: "Record Deleted",
        description: "The bill has been removed from history."
      });
      
      setHistoryDeleteDialogOpen(false);
      
      # If we were viewing this bill's details, close that too
      if (selectedBill && selectedBill === savedBills[historyDeleteIndex]) {
        setSelectedBill(null);
      }
    }
  };

  # Generate PDF for sharing
  const generatePDF = () => {
    if (!selectedBill) return;
    
    # Here we would normally use a PDF generation library
    # For this implementation, we'll just show a toast
    toast({
      title: "PDF Generated",
      description: `PDF for ${selectedBill.name}'s bill is ready for sharing.`
    });
  };

  # Handle login
  const handleLogin = () => {
    # Here we would normally integrate with Google Auth
    setUserLoggedIn(!userLoggedIn);
    toast({
      title: userLoggedIn ? "Logged Out" : "Logged In",
      description: userLoggedIn ? "You have been logged out." : "You have been logged in with Google."
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header with Login */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Billing Calculator</h1>
          <Button onClick={handleLogin} variant="outline">
            {userLoggedIn ? "Logout" : "Login with Google"}
          </Button>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Name Input Section */}
        <div className="mb-6 bg-white p-6 rounded-lg shadow-sm">
          <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
            <label htmlFor="customer-name" className="font-semibold text-gray-700 min-w-32">
              Customer Name:
            </label>
            <Input 
              id="customer-name"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              placeholder="Enter customer name"
              className="flex-grow max-w-md"
            />
          </div>
        </div>
        
        {/* Calculators */}
        <div className="space-y-8">
          {calculators.map((calcId, index) => (
            <BillingCalculator 
              key={calcId}
              id={calcId}
              isFirst={index === 0}
              onDelete={() => deleteCalculator(calcId)}
              onCalculationUpdate={(data) => updateCalculationData(calcId, data)}
              initialData={calculationData[calcId]}
            />
          ))}
        </div>
        
        {/* Add Calculator Button */}
        <div className="mt-8 flex justify-center">
          <Button 
            onClick={addCalculator} 
            className="rounded-full h-16 w-16"
            variant="outline"
          >
            ADD
          </Button>
        </div>
        
        {/* Total Bill Section */}
        <div className="mt-8 bg-white p-6 rounded-lg shadow-sm">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <span className="font-bold text-lg">Total Bill:</span>
            <Input 
              value={calculateTotalBill().toFixed(2)}
              className="font-bold text-lg max-w-md"
              readOnly
            />
          </div>
        </div>
        
        {/* Action Buttons */}
        <div className="mt-8 flex flex-wrap gap-4 justify-center">
          <Button onClick={viewHistory} variant="secondary">History</Button>
          <Button onClick={saveBill} variant="default">Save</Button>
          <Button onClick={generatePDF} variant="default">Print</Button>
        </div>
        
        {/* Advertisement Space */}
        <div className="mt-12 bg-gray-200 p-4 text-center rounded-md">
          <p className="text-gray-600">Advertisement Space</p>
          <div className="h-32 flex items-center justify-center border border-dashed border-gray-400">
            <p className="text-gray-500">Google AdSense Ad Unit</p>
          </div>
        </div>
      </div>

      {/* Confirmation Dialog for Calculator Deletion */}
      <Dialog open={confirmDialogOpen} onOpenChange={setConfirmDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
          </DialogHeader>
          <p>Are you sure you want to delete this calculator?</p>
          <DialogFooter className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setConfirmDialogOpen(false)}>No</Button>
            <Button variant="destructive" onClick={confirmDelete}>Yes, Delete</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* History Dialog */}
      <Dialog open={historyDialogOpen} onOpenChange={setHistoryDialogOpen}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Bill History</DialogTitle>
          </DialogHeader>
          
          <div className="my-4">
            <div className="relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
              <Input 
                placeholder="Search by customer name"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          
          {filteredBills.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No bills found</div>
          ) : (
            <div className="max-h-96 overflow-y-auto">
              {filteredBills.map((bill, index) => (
                <div 
                  key={`${bill.name}-${index}`}
                  className="p-3 border-b last:border-b-0 flex justify-between items-center hover:bg-gray-50 cursor-pointer"
                  onClick={() => viewBillDetails(bill)}
                >
                  <div>
                    <p className="font-medium">{bill.name}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(bill.date).toLocaleDateString()} • 
                      {bill.calculations.length} item{bill.calculations.length !== 1 ? 's' : ''} • 
                      ₹{bill.totalBill.toFixed(2)}
                    </p>
                  </div>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      setHistoryDeleteIndex(index);
                      setHistoryDeleteDialogOpen(true);
                    }}
                  >
                    <Trash2 size={18} />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Bill Details Dialog */}
      {selectedBill && (
        <Dialog open={!!selectedBill} onOpenChange={(open) => !open && setSelectedBill(null)}>
          <DialogContent className="max-w-3xl">
            <DialogHeader>
              <DialogTitle>{selectedBill.name}'s Bill</DialogTitle>
            </DialogHeader>
            
            <div className="my-4">
              <p className="text-gray-500 mb-4">
                Date: {new Date(selectedBill.date).toLocaleString()}
              </p>
              
              <div className="space-y-4">
                {selectedBill.calculations.map((calc, index) => (
                  <Card key={`${calc.id}-${index}`}>
                    <CardHeader>
                      <CardTitle>
                        {calc.productName || `Product ${index + 1}`}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <p>
                          Amount: {calc.amount} / {calc.amountUnit} × {calc.amountQty} = 
                          ₹{(calc.amount * calc.amountQty).toFixed(2)}
                        </p>
                        <p>
                          GST: {calc.gst}% = 
                          ₹{((calc.amount * calc.amountQty * calc.gst) / 100).toFixed(2)}
                        </p>
                        <p>
                          Transport: {calc.transport} / {calc.transportUnit} × {calc.transportQty} = 
                          ₹{(calc.transport * calc.transportQty).toFixed(2)}
                        </p>
                      </div>
                    </CardContent>
                    <CardFooter>
                      <p className="font-bold">
                        Subtotal: ₹{calc.total.toFixed(2)}
                      </p>
                    </CardFooter>
                  </Card>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-md">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-lg">Total Amount:</span>
                  <span className="font-bold text-lg">₹{selectedBill.totalBill.toFixed(2)}</span>
                </div>
              </div>
            </div>
            
            <DialogFooter className="flex justify-between">
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  className="flex gap-2 items-center" 
                  onClick={generatePDF}
                >
                  <Download size={18} />
                  Download PDF
                </Button>
                <Button 
                  variant="outline" 
                  className="flex gap-2 items-center"
                  onClick={() => {
                    toast({
                      title: "Share Option",
                      description: "Sharing functionality would be implemented here."
                    });
                  }}
                >
                  <Share2 size={18} />
                  Share
                </Button>
              </div>
              <Button onClick={() => setSelectedBill(null)}>Close</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}

      {/* History Delete Confirmation Dialog */}
      <Dialog open={historyDeleteDialogOpen} onOpenChange={setHistoryDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Delete</DialogTitle>
          </DialogHeader>
          <p>Are you sure you want to delete this bill from history?</p>
          <DialogFooter className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setHistoryDeleteDialogOpen(false)}>No</Button>
            <Button variant="destructive" onClick={confirmHistoryDelete}>Yes, Delete</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Index;
